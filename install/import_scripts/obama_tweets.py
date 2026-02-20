import csv
import re
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Final

from openatlas import app
from openatlas.models.entity import Entity, insert

FILE_PATH: Final = Path("install/import_scripts/obama_personal.csv")


@dataclass
class Entry:
    tweet_id: str
    tweet_link: str
    timestamp: datetime
    text: str
    hashtags: list[str | None]
    usernames: list[str | None]


def import_csv_data(file_path: Path) -> list[Entry]:
    entries_csv: list[Entry] = []
    with open(file_path, mode="r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f, delimiter=";")
        for row in reader:
            entries_csv.append(process_row(row))
    return entries_csv


def process_row(row: dict[str, str]) -> Entry:
    tweet_id: str = row.get("tweet_id", "").strip()
    tweet_link: str = row.get("tweet_link", "").strip()
    timestamp_str: str = row.get("timestamp", "").strip()
    text: str = row.get("text", "").strip()

    return Entry(
        tweet_id=tweet_id,
        tweet_link=tweet_link,
        timestamp=datetime.strptime(timestamp_str, "%Y/%m/%d_%H:%M"),
        text=text,
        hashtags=re.findall(r"#\w+", text),
        usernames=re.findall(r"@\w+", text))


def get_hashtag_types(entries_: list[Entry]) -> dict[str, Entity]:
    hashtag_types_: dict[str, Entity] = {}
    for entry_ in entries_:
        for hashtag_ in entry_.hashtags:
            if hashtag_ in hashtag_types_:
                continue
            type_ = insert({
                'name': hashtag_,
                'openatlas_class_name': 'type'})
            type_.link('P127', hashtag_hierarchy)
            hashtag_types_[hashtag_] = type_
    return hashtag_types_


def get_account_types(entries_: list[Entry]) -> dict[str, Entity]:
    account_types_: dict[str, Entity] = {}
    for entry_ in entries_:
        for username_ in entry_.usernames:
            if username_ in account_types_:
                continue
            type_ = insert({
                'name': username_,
                'openatlas_class_name': 'type'})
            type_.link('P127', account_hierarchy)
            account_types_[username_] = type_
    return account_types_


with app.test_request_context():
    app.preprocess_request()
    sources = Entity.get_by_class('source')
    type_ = Entity.get_by_id(1314)
    for source in sources:
        source.link('P2', type_)


    1/0
    entries = import_csv_data(FILE_PATH)
    source_type = Entity.get_by_id(129)
    link_type = Entity.get_by_id(10)
    hashtag_hierarchy = Entity.get_by_id(247)
    account_hierarchy = Entity.get_by_id(134)

    hashtag_types = get_hashtag_types(entries)
    account_types = get_account_types(entries)

    for entry in entries:
        tweet_name = f'{entry.timestamp.strftime('%Y-%m-%d')} Tweet'
        tweet = insert({
            'name': tweet_name,
            'description': entry.text,
            'openatlas_class_name': 'source'})
        tweet.link('P2', source_type)

        if entry.hashtags:
            for hashtag in entry.hashtags:
                hashtag_type = hashtag_types.get(hashtag)
                if hashtag_type:
                    tweet.link('P2', hashtag_type)

        twitter_link = insert({
            'name': entry.tweet_link,
            'openatlas_class_name': 'external_reference'})
        twitter_link.link('P2', link_type)
        twitter_link.link('P67', tweet)

        creation = insert({
            'name': f'{entry.timestamp.strftime('%Y-%m-%d')} Writing',
            'openatlas_class_name': 'creation',
            'begin_from': entry.timestamp})

        if entry.usernames:
            for username in entry.usernames:
                account_type = account_types.get(username)
                if account_type:
                    creation.link('P2', account_type)

        creation.link('P94', tweet)
