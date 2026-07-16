import glob
import json
import os
import re
from flask import g
from openatlas import app

# List of all allowed languages in tags
ALLOWED_LANGS = ("de", "en", "cz", "la", "fr", "sl")
VALID_TAGS = set(f"##{lang}_##" for lang in ALLOWED_LANGS) | set(f"##_{lang}##" for lang in ALLOWED_LANGS)


def classify_mismatch(text: str) -> str:
    """
    Categorize a mismatching description into a specific mismatch sub-category:
    - 'mismatch_open_tag_used_as_close': Open tags used as close tags (e.g. ##en_##...##en_##).
    - 'mismatch_opening_without_closing': Has opening tag but no closing tag of that language.
    - 'mismatch_closing_without_opening': Has closing tag but no opening tag of that language.
    - 'mismatch_duplicated_open_tags': Duplicate open tags next to each other (e.g. ##de_####de_##).
    - 'mismatch_nesting_error': Mismatched tag nesting (e.g. ##en_##...##_de##).
    - 'mismatch_general': Other syntax errors or general mismatches.
    """
    if not text:
        return "mismatch_general"

    # 1. Check for duplicate/adjacent open tags (double tagging, e.g. ##en_####en_##).
    # This must be checked before the generic "open tag used as close" case below,
    # otherwise two identical adjacent open tags would be misclassified.
    for lang in ALLOWED_LANGS:
        # Directly adjacent duplicate open tags, e.g. ##en_####en_##.
        if f"##{lang}_####{lang}_##" in text:
            return "mismatch_duplicated_open_tags"
        # Same open tag repeated (with content in between), e.g. ##en_##...##en_##,
        # without any closing tag anywhere.
        if len(re.findall(rf"##{lang}_##", text)) > 1 and f"##_{lang}##" not in text:
            # Distinguish "double tagging" (repeated open tags with no unique text
            # that belongs together) from open-tag-used-as-close. If any two
            # occurrences are directly adjacent it is double tagging.
            if re.search(rf"(##{lang}_##){{2,}}", text):
                return "mismatch_duplicated_open_tags"

    # 2. Check for duplicate/repeated open tags used to close (e.g. ##en_## ... ##en_##)
    for lang in ALLOWED_LANGS:
        if len(re.findall(rf"##{lang}_##", text)) > 1 and f"##_{lang}##" not in text:
            return "mismatch_open_tag_used_as_close"

    # 3. Check for opening tags without a closing tag
    for lang in ALLOWED_LANGS:
        if f"##{lang}_##" in text and f"##_{lang}##" not in text:
            return "mismatch_opening_without_closing"

    # 4. Check for closing tags without an opening tag
    for lang in ALLOWED_LANGS:
        if f"##_{lang}##" in text and f"##{lang}_##" not in text:
            return "mismatch_closing_without_opening"

    # 5. Check for mismatched nesting (e.g. en open, de close)
    parts = text.split("##")
    stack = []
    for i, part in enumerate(parts):
        if i % 2 == 1:
            if part.endswith("_") and part[:-1] in ALLOWED_LANGS:
                stack.append(part[:-1])
            elif part.startswith("_") and part[1:] in ALLOWED_LANGS:
                if not stack or stack[-1] != part[1:]:
                    return "mismatch_nesting_error"
                stack.pop()

    return "mismatch_general"


def clean_and_translate_old(desc: str) -> str:
    """
    Cleans up old translation formatting:
    splits at the old system language tag (e.g. ##German),
    wraps the text before in ##en_##...##_en## and after in ##de_##...##_de##,
    and handles the 'Ramsauer' reference block.
    """
    if not desc:
        return ""

    old_patterns = [
        "german", "deutsch", "germam", "germna",
        "gerrman", "geerman", "geman", "geran",
        "germa", "gernan", "gderman"
    ]
    combined_pattern = re.compile(r"(?<!de_|en_)##(" + "|".join(old_patterns) + r")\b", re.IGNORECASE)
    parts = combined_pattern.split(desc, maxsplit=1)
    if len(parts) < 3:
        return desc

    before = parts[0].strip()
    after = parts[2].strip()

    # Check for Ramsauer in the German text
    match = re.search(r'\bramsauer\b', after, re.IGNORECASE)
    if match:
        start_idx = match.start()
        german_translation = after[:start_idx].strip()
        untagged_text = after[start_idx:].strip()

        if before and german_translation:
            return f"##en_##\r\n{before}\r\n##_en##\r\n\r\n##de_##\r\n{german_translation}\r\n##_de##\r\n\r\n{untagged_text}"
        elif before:
            return f"##en_##\r\n{before}\r\n##_en##\r\n\r\n{untagged_text}"
        elif german_translation:
            return f"##de_##\r\n{german_translation}\r\n##_de##\r\n\r\n{untagged_text}"
        else:
            return untagged_text

    if before and after:
        return f"##en_##\r\n{before}\r\n##_en##\r\n\r\n##de_##\r\n{after}\r\n##_de##"
    elif before:
        return f"##en_##\r\n{before}\r\n##_en##"
    elif after:
        return f"##de_##\r\n{after}\r\n##_de##"
    return ""


# Old-system language markers (e.g. "##English", "##Czech", "##German")
# mapped to the modern language code they should become.
OLD_LANG_MARKERS = {
    "en": ["english", "englisch"],
    "de": [
        "german", "deutsch", "germam", "germna", "gerrman",
        "geerman", "geman", "geran", "germa", "gernan", "gderman"
    ],
    "cz": ["czech", "tschechisch", "tschechische", "cesky", "cesky"],
}
# Reverse lookup: marker word -> language code.
OLD_MARKER_TO_LANG = {
    word: lang for lang, words in OLD_LANG_MARKERS.items() for word in words
}
# Regex matching any old-system language marker (e.g. ##English, ##Czech, ##German).
ALL_OLD_MARKER_REGEX = re.compile(
    r"(?<!_)##(" + "|".join(OLD_MARKER_TO_LANG.keys()) + r")\b",
    re.IGNORECASE
)
# Regex matching a proper opening language tag (e.g. ##en_##).
PROPER_OPEN_TAG_REGEX = re.compile(
    r"##(?:" + "|".join(ALLOWED_LANGS) + r")_##",
    re.IGNORECASE
)


def clean_old_lang_markers(desc: str) -> str:
    """
    Convert descriptions that mix proper language tags with old-system
    language markers (e.g. ##English, ##Czech, ##German) into cleanly
    tagged blocks. Text is grouped by language and each block is wrapped
    in ##xx_## ... ##_xx##.
    """
    if not desc:
        return ""

    all_markers = "|".join(OLD_MARKER_TO_LANG.keys())
    langs = "|".join(ALLOWED_LANGS)
    token_re = re.compile(
        r"(##(?:(?:" + langs + r")_|_(?:" + langs + r"))##"
        r"|##(?:" + all_markers + r")\b)",
        re.IGNORECASE
    )

    blocks = []
    current_lang = None
    current_text = ""

    def flush():
        nonlocal current_text
        if current_lang and current_text.strip():
            blocks.append((current_lang, current_text.strip()))
        current_text = ""

    for token in token_re.split(desc):
        if not token:
            continue
        low = token.lower()
        if token_re.fullmatch(token):
            inner = token[2:].rstrip("#").rstrip()
            if inner.startswith("_"):
                # Closing tag: close current block.
                flush()
                current_lang = None
            elif inner.endswith("_"):
                # Proper opening tag.
                flush()
                current_lang = inner[:-1].lower()
            else:
                # Old-system marker word.
                flush()
                current_lang = OLD_MARKER_TO_LANG[low[2:].strip()]
        else:
            current_text += token
    flush()

    if not blocks:
        return ""

    return "\r\n\r\n".join(
        f"##{lang}_##\r\n{text}\r\n##_{lang}##" for lang, text in blocks
    )


def clean_missing_hash(desc: str) -> str:
    """
    Cleans up missing hash tag typos (e.g. #de_## or ##en_#) by replacing them
    with standard double hash tags (e.g. ##de_## or ##en_##) for all allowed languages.
    """
    if not desc:
        return ""

    langs_pattern = "|".join(f"{lang}_" for lang in ALLOWED_LANGS) + "|" + "|".join(f"_{lang}" for lang in ALLOWED_LANGS)

    def replace_start(match):
        return f"##{match.group(1)}##"
    text = re.sub(rf"(?<!#)#({langs_pattern})##(?!#)", replace_start, desc, flags=re.IGNORECASE)

    def replace_end(match):
        return f"##{match.group(1)}##"
    text = re.sub(rf"(?<!#)##({langs_pattern})#(?!#)", replace_end, text, flags=re.IGNORECASE)

    return text


def clean_opening_without_closing(desc: str) -> str:
    """
    Inserts missing closing tags (e.g. ##_en## or ##_de##) at the appropriate boundaries.
    """
    if not desc:
        return ""

    text = desc.strip()

    # Normalize single-hash dangling endings like ##_en or ##_de for all allowed languages
    for lang in ALLOWED_LANGS:
        text = re.sub(rf"##_{lang}$", f"##_{lang}##", text, flags=re.IGNORECASE)

    # Split by tags, keeping the tags.
    tag_regex = re.compile(rf"##(?:(?:{'|'.join(ALLOWED_LANGS)})_|_(?:{'|'.join(ALLOWED_LANGS)}))##", re.IGNORECASE)
    parts = tag_regex.split(text)
    tags = tag_regex.findall(text)

    # Rebuild the string, inserting missing closing tags where needed.
    new_parts = []
    open_stack = []

    for i in range(len(parts)):
        new_parts.append(parts[i])
        if i < len(tags):
            tag = tags[i]
            # Parse tag content (e.g. "de_" or "_de")
            tag_content = tag[2:-2]
            if tag_content.endswith("_"):
                lang = tag_content[:-1]
                # If another tag is open, close it first before opening this one!
                while open_stack:
                    popped = open_stack.pop()
                    new_parts.append(f"##_{popped}##\r\n\r\n")
                open_stack.append(lang)
                new_parts.append(tag)
            else:
                lang = tag_content[1:]
                if lang in open_stack:
                    # Close any nested/open tags up to this one
                    while open_stack:
                        popped = open_stack.pop()
                        new_parts.append(f"##_{popped}##" if popped == lang else f"##_{popped}##\r\n\r\n")
                        if popped == lang:
                            break
                else:
                    # Closing tag without opening, just append it
                    new_parts.append(tag)

    # At the end of the text, close any remaining open tags
    while open_stack:
        popped = open_stack.pop()
        new_parts.append(f"\r\n##_{popped}##")

    return "".join(new_parts)


def clean_open_tag_used_as_close(desc: str) -> str:
    """
    Replaces duplicate opening tags used as closing tags (e.g. the second ##en_##) with standard closing tags (e.g. ##_en##) for all allowed languages.
    """
    if not desc:
        return ""

    text = desc

    for lang in ALLOWED_LANGS:
        if f"##_{lang}##" not in desc:
            matches = list(re.finditer(rf"##{lang}_##", text, flags=re.IGNORECASE))
            if len(matches) >= 2:
                start, end = matches[1].span()
                text = text[:start] + f"##_{lang}##" + text[end:]

    return text


def classify_description(text: str) -> str | None:
    """
    Classify the description of an entity based on the structure of language tags:
    - 'old_translation': Description contains old system tags (like "##German", "##german", "##Deutsch").
    - 'missing_hash': Description has language tags missing one of their hash symbols (e.g. #de_## or ##en_#).
    - 'license_tag': Description has license url tags (e.g. ##licenseUrl_##).
    - 'tag_whitespace': Description has language tags with spacing typos (e.g. ## de_##).
    - 'tag_missing_underscore': Description has language tags missing their underscores (e.g. ##de##).
    - 'no_lang_tag': Description has text block directly wrapped in double hashes (e.g. ##Wellenbandtopf...##).
    - 'correct': Tag is opened and closed correctly, and no other text is "around" the tags
                 (unless both German and English tags are present).
    - 'only_one_translation': Description has only one of the modern language tags (English-only or German-only).
    - 'mismatch_opening_without_closing': Has opening tag but no closing tag.
    - 'mismatch_open_tag_used_as_close': Open tags used as close tags.
    - 'mismatch_closing_without_opening': Has closing tag but no opening tag.
    - 'mismatch_duplicated_open_tags': Duplicate open tags next to each other.
    - 'mismatch_nesting_error': Mismatched tag nesting.
    - 'mismatch_general': Other syntax errors or general mismatches.
    """
    if not text:
        return classify_mismatch(text)

    # 1. Ignore ##RCD completely.
    # Replace all occurrences of ##RCD (case-insensitive) with empty string.
    # If there are no other translation-like/double-hash elements left, we ignore the entry completely.
    clean_text = re.sub(r'##RCD', '', text, flags=re.IGNORECASE)

    # Check if there is any other double-hash or single-hash typo remaining.
    # If not, ignore the description.
    langs_pattern = "|".join(f"{lang}_" for lang in ALLOWED_LANGS) + "|" + "|".join(f"_{lang}" for lang in ALLOWED_LANGS)
    missing_hash_pattern = re.compile(
        rf"(?<!#)#({langs_pattern})##(?!#)|(?<!#)##({langs_pattern})#(?!#)",
        re.IGNORECASE
    )
    if '##' not in clean_text and not missing_hash_pattern.search(clean_text):
        old_patterns = [
            "german", "deutsch", "germam", "germna",
            "gerrman", "geerman", "geman", "geran",
            "germa", "gernan", "gderman"
        ]
        old_regex = re.compile(r"(?<!de_|en_)##(" + "|".join(old_patterns) + r")\b", re.IGNORECASE)
        if not old_regex.search(clean_text):
            return None

    lower_desc = clean_text.lower()

    # 1b. Check for old-system language markers (e.g. ##English, ##Czech, ##German)
    # that appear alongside proper language tags. These can be automatically
    # converted into clean language blocks. Untagged old-only descriptions
    # (no proper ##xx_## tag) are handled by 'old_translation' below.
    if PROPER_OPEN_TAG_REGEX.search(clean_text) and ALL_OLD_MARKER_REGEX.search(clean_text):
        return "old_lang_marker"

    # 2. Check for old translation system typos and variants
    old_patterns = [
        "german", "deutsch", "germam", "germna",
        "gerrman", "geerman", "geman", "geran",
        "germa", "gernan", "gderman"
    ]
    old_regex = re.compile(r"(?<!de_|en_)##(" + "|".join(old_patterns) + r")\b", re.IGNORECASE)
    if old_regex.search(clean_text):
        return "old_translation"

    # 3. Check for missing hash typos (e.g. #de_##, ##en_#, etc.)
    if missing_hash_pattern.search(clean_text):
        return "missing_hash"

    # 4. Check for license tags (e.g. ##licenseUrl_##)
    if "licenseurl" in lower_desc:
        return "license_tag"

    # 5. Check for invalid/custom tags or patterns
    tags = re.findall(r'##[^#]+##', clean_text)
    invalid_tags = [t for t in tags if t not in VALID_TAGS]
    if invalid_tags:
        for tag in invalid_tags:
            tag_clean = re.sub(r'\s+', '', tag.lower())
            if tag_clean in VALID_TAGS:
                return "tag_whitespace"
            tag_stripped = tag.strip("# ").lower()
            if tag_stripped in ALLOWED_LANGS or (tag_stripped.endswith("_") and tag_stripped[:-1] in ALLOWED_LANGS) or (tag_stripped.startswith("_") and tag_stripped[1:] in ALLOWED_LANGS):
                return "tag_missing_underscore"
        return "no_lang_tag"

    parts = clean_text.split("##")
    if len(parts) % 2 == 0:
        # Odd number of ##. The last ## is dangling.
        # If it is followed by a word (e.g. ##RCD), it's custom_tags.
        # Otherwise, it's mismatch_code.
        word_match = re.match(r'^[a-zA-ZÄÖÜäöüß]+', parts[-1])
        if word_match and not any(parts[-1].startswith((f"{lang}_", f"_{lang}")) for lang in ALLOWED_LANGS):
            full_tag = f"##{parts[-1]}##"
            tag_clean = re.sub(r'\s+', '', full_tag.lower())
            if tag_clean in VALID_TAGS:
                return "tag_whitespace"
            tag_stripped = parts[-1].strip().lower()
            if tag_stripped in ALLOWED_LANGS or (tag_stripped.endswith("_") and tag_stripped[:-1] in ALLOWED_LANGS) or (tag_stripped.startswith("_") and tag_stripped[1:] in ALLOWED_LANGS):
                return "tag_missing_underscore"
            return "no_lang_tag"
        return classify_mismatch(clean_text)

    # 6. Check tag mismatch / unclosed tags / structure
    stack = []
    has_text_outside = False
    inside_block = False
    languages_seen = set()

    for i, part in enumerate(parts):
        if i % 2 == 1:
            # Odd index: Tag content
            if part.endswith("_") and part[:-1] in ALLOWED_LANGS:
                lang = part[:-1]
                if lang in stack:
                    # Duplicate open tag used to close, or invalid nesting
                    return classify_mismatch(clean_text)
                stack.append(lang)
                languages_seen.add(lang)
                inside_block = True
            elif part.startswith("_") and part[1:] in ALLOWED_LANGS:
                lang = part[1:]
                if not stack:
                    return classify_mismatch(clean_text)
                popped = stack.pop()
                if popped != lang:
                    return classify_mismatch(clean_text)
                if not stack:
                    inside_block = False
            else:
                full_tag = f"##{part}##"
                tag_clean = re.sub(r'\s+', '', full_tag.lower())
                if tag_clean in VALID_TAGS:
                    return "tag_whitespace"
                tag_stripped = part.strip().lower()
                if tag_stripped in ALLOWED_LANGS or (tag_stripped.endswith("_") and tag_stripped[:-1] in ALLOWED_LANGS) or (tag_stripped.startswith("_") and tag_stripped[1:] in ALLOWED_LANGS):
                    return "tag_missing_underscore"
                return "no_lang_tag"
        else:
            # Even index: Text outside or between tags
            if part.strip() != "":
                if not inside_block:
                    has_text_outside = True

    if stack:
        return classify_mismatch(clean_text)

    if len(languages_seen) == 1:
        return "only_one_translation"

    return "correct"


with app.test_request_context():
    app.preprocess_request()

    g.cursor.execute(
        """
        SELECT id, name, description
        FROM model.entity
        WHERE description LIKE %(term)s;
        """,
        {"term": "%##%"}
    )

    # Store in memory (a list of dictionaries)
    entities = [
        {
            "id": row["id"],
            "name": row["name"],
            "description": row["description"]
        }
        for row in g.cursor
    ]

# Differentiate the entities into categories
categories = {
    "correct": [],
    "only_one_translation": [],
    "old_translation": [],
    "old_lang_marker": [],
    "missing_hash": [],
    "license_tag": [],
    "tag_whitespace": [],
    "tag_missing_underscore": [],
    "no_lang_tag": [],
    "mismatch_opening_without_closing": [],
    "mismatch_open_tag_used_as_close": [],
    "mismatch_closing_without_opening": [],
    "mismatch_duplicated_open_tags": [],
    "mismatch_nesting_error": [],
    "mismatch_general": []
}

for entity in entities:
    category = classify_description(entity["description"])
    if category is not None:
        categories[category].append(entity)

# Write lists to JSON files in the same folder
base_path = os.path.dirname(os.path.abspath(__file__))

# First delete any existing thanados_* JSON and CSV files
for pattern in ("thanados_*.json", "thanados_*.csv"):
    for old_file in glob.glob(os.path.join(base_path, pattern)):
        try:
            os.remove(old_file)
            print(f"Deleted old file: {os.path.basename(old_file)}")
        except OSError as e:
            print(f"Error deleting {old_file}: {e}")

for category_name, list_of_entities in categories.items():
    if not list_of_entities:
        continue

    # Write JSON with links as URLs
    json_entities = []
    for entity in list_of_entities:
        entity_copy = entity.copy()
        entity_copy["url"] = f"https://thanados.openatlas.eu/update/{entity['id']}"

        # Apply translation/correction logic depending on category
        if category_name == "old_translation":
            entity_copy["description_translated"] = clean_and_translate_old(entity["description"])
        elif category_name == "old_lang_marker":
            entity_copy["description_translated"] = clean_old_lang_markers(entity["description"])
        elif category_name == "missing_hash":
            entity_copy["description_translated"] = clean_missing_hash(entity["description"])
        elif category_name == "mismatch_opening_without_closing":
            entity_copy["description_translated"] = clean_opening_without_closing(entity["description"])
        elif category_name == "mismatch_open_tag_used_as_close":
            entity_copy["description_translated"] = clean_open_tag_used_as_close(entity["description"])

        json_entities.append(entity_copy)

    output_filename = f"thanados_{category_name}.json"
    output_path = os.path.join(base_path, output_filename)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(json_entities, f, ensure_ascii=False, indent=4)
    print(f"Saved {len(json_entities)} entities to {output_path}")

# Merge all automatically corrected categories into one file
corrected_categories = [
    "old_translation",
    "old_lang_marker",
    "missing_hash",
    "mismatch_opening_without_closing",
    "mismatch_open_tag_used_as_close"
]
all_corrected_entities = []
for cat in corrected_categories:
    list_of_entities = categories[cat]
    for entity in list_of_entities:
        entity_copy = entity.copy()
        entity_copy["url"] = f"https://thanados.openatlas.eu/entity/{entity['id']}"
        if cat == "old_translation":
            entity_copy["description_translated"] = clean_and_translate_old(entity["description"])
        elif cat == "old_lang_marker":
            entity_copy["description_translated"] = clean_old_lang_markers(entity["description"])
        elif cat == "missing_hash":
            entity_copy["description_translated"] = clean_missing_hash(entity["description"])
        elif cat == "mismatch_opening_without_closing":
            entity_copy["description_translated"] = clean_opening_without_closing(entity["description"])
        elif cat == "mismatch_open_tag_used_as_close":
            entity_copy["description_translated"] = clean_open_tag_used_as_close(entity["description"])

        # Safety: never emit a correction that would blank the description
        # or that does not actually change anything.
        translated = entity_copy.get("description_translated", "")
        if not translated or not translated.strip():
            print(f"Skipping entity {entity['id']} ({cat}): empty translation result.")
            continue
        if translated == entity["description"]:
            continue
        all_corrected_entities.append(entity_copy)

if all_corrected_entities:
    output_filename = "thanados_all_corrected.json"
    output_path = os.path.join(base_path, output_filename)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(all_corrected_entities, f, ensure_ascii=False, indent=4)
    print(f"Saved {len(all_corrected_entities)} merged corrected entities to {output_path}")
