import csv
import glob
import json
import os
import re
from flask import g
from openatlas import app


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

    # 1. Check for duplicate/repeated open tags used to close (e.g. ##en_## ... ##en_##)
    if len(re.findall(r"##en_##", text)) > 1 and "##_en##" not in text:
        return "mismatch_open_tag_used_as_close"
    if len(re.findall(r"##de_##", text)) > 1 and "##_de##" not in text:
        return "mismatch_open_tag_used_as_close"

    # 2. Check for duplicate nested open tags (e.g. ##de_####de_##)
    if "##de_####de_##" in text or "##en_####en_##" in text:
        return "mismatch_duplicated_open_tags"

    # 3. Check for opening tags without a closing tag
    has_open_de = "##de_##" in text
    has_close_de = "##_de##" in text
    has_open_en = "##en_##" in text
    has_close_en = "##_en##" in text

    if has_open_de and not has_close_de:
        return "mismatch_opening_without_closing"
    if has_open_en and not has_close_en:
        return "mismatch_opening_without_closing"

    # 4. Check for closing tags without an opening tag
    if has_close_de and not has_open_de:
        return "mismatch_closing_without_opening"
    if has_close_en and not has_open_en:
        return "mismatch_closing_without_opening"

    # 5. Check for mismatched nesting (e.g. en open, de close)
    parts = text.split("##")
    stack = []
    for i, part in enumerate(parts):
        if i % 2 == 1:
            if part in ("de_", "en_"):
                stack.append(part[:-1])
            elif part in ("_de", "_en"):
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


def clean_missing_hash(desc: str) -> str:
    """
    Cleans up missing hash tag typos (e.g. #de_## or ##en_#) by replacing them
    with standard double hash tags (e.g. ##de_## or ##en_##).
    """
    if not desc:
        return ""

    def replace_start(match):
        return f"##{match.group(1)}##"
    text = re.sub(r"(?<!#)#(de_|en_|_de|_en)##(?!#)", replace_start, desc, flags=re.IGNORECASE)

    def replace_end(match):
        return f"##{match.group(1)}##"
    text = re.sub(r"(?<!#)##(de_|en_|_de|_en)#(?!#)", replace_end, text, flags=re.IGNORECASE)

    return text


def clean_opening_without_closing(desc: str) -> str:
    """
    Inserts missing closing tags (e.g. ##_en## or ##_de##) at the appropriate boundaries.
    """
    if not desc:
        return ""

    # Normalize single-hash dangling endings like ##_en or ##_de
    text = re.sub(r"##_en$", "##_en##", desc.strip(), flags=re.IGNORECASE)
    text = re.sub(r"##_de$", "##_de##", text, flags=re.IGNORECASE)

    has_en_open = "##en_##" in text
    has_en_close = "##_en##" in text
    has_de_open = "##de_##" in text
    has_de_close = "##_de##" in text

    if has_en_open and has_de_open:
        idx_en_open = text.find("##en_##")
        idx_de_open = text.find("##de_##")

        if idx_en_open < idx_de_open:
            if not has_en_close or text.find("##_en##") > idx_de_open:
                text = text.replace("##de_##", "##_en##\r\n\r\n##de_##", 1)
            if not "##_de##" in text[idx_de_open:]:
                text = text.strip() + "\r\n##_de##"
        else:
            if not has_de_close or text.find("##_de##") > idx_en_open:
                text = text.replace("##en_##", "##_de##\r\n\r\n##en_##", 1)
            if not "##_en##" in text[idx_en_open:]:
                text = text.strip() + "\r\n##_en##"

    elif has_en_open and not has_de_open:
        if not has_en_close:
            text = text.strip() + "\r\n##_en##"

    elif has_de_open and not has_en_open:
        if not has_de_close:
            text = text.strip() + "\r\n##_de##"

    return text


def clean_open_tag_used_as_close(desc: str) -> str:
    """
    Replaces duplicate opening tags used as closing tags (e.g. the second ##en_##) with standard closing tags (e.g. ##_en##).
    """
    if not desc:
        return ""

    text = desc

    # Replaces the second occurrence of ##en_## if ##_en## is not in original description
    if "##_en##" not in desc:
        en_matches = list(re.finditer(r"##en_##", text, flags=re.IGNORECASE))
        if len(en_matches) >= 2:
            start, end = en_matches[1].span()
            text = text[:start] + "##_en##" + text[end:]

    # Replaces the second occurrence of ##de_## if ##_de## is not in original description
    if "##_de##" not in desc:
        de_matches = list(re.finditer(r"##de_##", text, flags=re.IGNORECASE))
        if len(de_matches) >= 2:
            start, end = de_matches[1].span()
            text = text[:start] + "##_de##" + text[end:]

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
    missing_hash_pattern = re.compile(
        r"(?<!#)#(de_|en_|_de|_en)##(?!#)|(?<!#)##(de_|en_|_de|_en)#(?!#)",
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
    invalid_tags = [t for t in tags if t not in ("##de_##", "##_de##", "##en_##", "##_en##")]
    if invalid_tags:
        for tag in invalid_tags:
            if re.sub(r'\s+', '', tag.lower()) in ("##de_##", "##_de##", "##en_##", "##_en##"):
                return "tag_whitespace"
            if tag.strip("# ").lower() in ("de", "en", "de_", "_de", "en_", "_en"):
                return "tag_missing_underscore"
        return "no_lang_tag"

    parts = clean_text.split("##")
    if len(parts) % 2 == 0:
        # Odd number of ##. The last ## is dangling.
        # If it is followed by a word (e.g. ##RCD), it's custom_tags.
        # Otherwise, it's mismatch_code.
        word_match = re.match(r'^[a-zA-ZÄÖÜäöüß]+', parts[-1])
        if word_match and not parts[-1].startswith(("de_", "en_", "_de", "_en")):
            full_tag = f"##{parts[-1]}##"
            if re.sub(r'\s+', '', full_tag.lower()) in ("##de_##", "##_de##", "##en_##", "##_en##"):
                return "tag_whitespace"
            if parts[-1].strip().lower() in ("de", "en", "de_", "_de", "en_", "_en"):
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
            if part in ("de_", "en_"):
                lang = part[:-1]
                if lang in stack:
                    # Duplicate open tag used to close, or invalid nesting
                    return classify_mismatch(clean_text)
                stack.append(lang)
                languages_seen.add(lang)
                inside_block = True
            elif part in ("_de", "_en"):
                if not stack:
                    return classify_mismatch(clean_text)
                popped = stack.pop()
                if popped != part[1:]:
                    return classify_mismatch(clean_text)
                if not stack:
                    inside_block = False
            else:
                full_tag = f"##{part}##"
                if re.sub(r'\s+', '', full_tag.lower()) in ("##de_##", "##_de##", "##en_##", "##_en##"):
                    return "tag_whitespace"
                if part.strip().lower() in ("de", "en", "de_", "_de", "en_", "_en"):
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

    if category_name == "no_lang_tag":
        # Write CSV
        output_filename_csv = f"thanados_{category_name}.csv"
        output_path_csv = os.path.join(base_path, output_filename_csv)
        with open(output_path_csv, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["id", "name", "description"])
            for entity in list_of_entities:
                link = f"https://thanados.openatlas.eu/entity/{entity['id']}"
                writer.writerow([link, entity["name"], entity["description"]])
        print(f"Saved {len(list_of_entities)} entities to {output_path_csv}")

        # Write JSON with links as IDs
        json_entities = []
        for entity in list_of_entities:
            entity_copy = entity.copy()
            entity_copy["id"] = f"https://thanados.openatlas.eu/entity/{entity['id']}"
            json_entities.append(entity_copy)

        output_filename_json = f"thanados_{category_name}.json"
        output_path_json = os.path.join(base_path, output_filename_json)
        with open(output_path_json, "w", encoding="utf-8") as f:
            json.dump(json_entities, f, ensure_ascii=False, indent=4)
        print(f"Saved {len(json_entities)} entities to {output_path_json}")
    elif category_name == "old_translation":
        # For old_translation, we add a new key "description_translated"
        translated_entities = []
        for entity in list_of_entities:
            entity_copy = entity.copy()
            entity_copy["description_translated"] = clean_and_translate_old(entity["description"])
            translated_entities.append(entity_copy)

        output_filename = f"thanados_{category_name}.json"
        output_path = os.path.join(base_path, output_filename)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(translated_entities, f, ensure_ascii=False, indent=4)
        print(f"Saved {len(translated_entities)} entities to {output_path}")
    elif category_name == "missing_hash":
        # For missing_hash, we add a new key "description_translated"
        translated_entities = []
        for entity in list_of_entities:
            entity_copy = entity.copy()
            entity_copy["description_translated"] = clean_missing_hash(entity["description"])
            translated_entities.append(entity_copy)

        output_filename = f"thanados_{category_name}.json"
        output_path = os.path.join(base_path, output_filename)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(translated_entities, f, ensure_ascii=False, indent=4)
        print(f"Saved {len(translated_entities)} entities to {output_path}")
    elif category_name == "mismatch_opening_without_closing":
        # For mismatch_opening_without_closing, we add a new key "description_translated"
        translated_entities = []
        for entity in list_of_entities:
            entity_copy = entity.copy()
            entity_copy["description_translated"] = clean_opening_without_closing(entity["description"])
            translated_entities.append(entity_copy)

        output_filename = f"thanados_{category_name}.json"
        output_path = os.path.join(base_path, output_filename)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(translated_entities, f, ensure_ascii=False, indent=4)
        print(f"Saved {len(translated_entities)} entities to {output_path}")
    elif category_name == "mismatch_open_tag_used_as_close":
        # For mismatch_open_tag_used_as_close, we add a new key "description_translated"
        translated_entities = []
        for entity in list_of_entities:
            entity_copy = entity.copy()
            entity_copy["description_translated"] = clean_open_tag_used_as_close(entity["description"])
            translated_entities.append(entity_copy)

        output_filename = f"thanados_{category_name}.json"
        output_path = os.path.join(base_path, output_filename)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(translated_entities, f, ensure_ascii=False, indent=4)
        print(f"Saved {len(translated_entities)} entities to {output_path}")
    elif category_name == "only_one_translation":
        # Write JSON with links as IDs
        json_entities = []
        for entity in list_of_entities:
            entity_copy = entity.copy()
            entity_copy["id"] = f"https://thanados.openatlas.eu/entity/{entity['id']}"
            json_entities.append(entity_copy)

        output_filename_json = f"thanados_{category_name}.json"
        output_path_json = os.path.join(base_path, output_filename_json)
        with open(output_path_json, "w", encoding="utf-8") as f:
            json.dump(json_entities, f, ensure_ascii=False, indent=4)
        print(f"Saved {len(json_entities)} entities to {output_path_json}")
    else:
        output_filename = f"thanados_{category_name}.json"
        output_path = os.path.join(base_path, output_filename)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(list_of_entities, f, ensure_ascii=False, indent=4)
        print(f"Saved {len(list_of_entities)} entities to {output_path}")

# Merge all automatically corrected categories into one file
corrected_categories = [
    "old_translation",
    "missing_hash",
    "mismatch_opening_without_closing",
    "mismatch_open_tag_used_as_close"
]
all_corrected_entities = []
for cat in corrected_categories:
    list_of_entities = categories[cat]
    for entity in list_of_entities:
        entity_copy = entity.copy()
        if cat == "old_translation":
            entity_copy["description_translated"] = clean_and_translate_old(entity["description"])
        elif cat == "missing_hash":
            entity_copy["description_translated"] = clean_missing_hash(entity["description"])
        elif cat == "mismatch_opening_without_closing":
            entity_copy["description_translated"] = clean_opening_without_closing(entity["description"])
        elif cat == "mismatch_open_tag_used_as_close":
            entity_copy["description_translated"] = clean_open_tag_used_as_close(entity["description"])
        all_corrected_entities.append(entity_copy)

if all_corrected_entities:
    output_filename = "thanados_all_corrected.json"
    output_path = os.path.join(base_path, output_filename)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(all_corrected_entities, f, ensure_ascii=False, indent=4)
    print(f"Saved {len(all_corrected_entities)} merged corrected entities to {output_path}")
