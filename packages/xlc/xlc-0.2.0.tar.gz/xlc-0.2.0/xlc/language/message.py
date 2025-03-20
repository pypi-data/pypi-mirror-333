# coding:utf-8

import os
from typing import Dict
from typing import Iterator

from xlc.database.langtags import LANGUAGES
from xlc.database.langtags import LangT  # noqa:H306
from xlc.database.langtags import LangTag
from xlc.language.segment import Segment


class Message():
    def __init__(self):
        self.__segments: Dict[LangTag, Segment] = {}

    def __iter__(self) -> Iterator[LangTag]:
        return iter(self.__segments)

    def __len__(self) -> int:
        return len(self.__segments)

    def __contains__(self, langtag: LangT) -> bool:
        return LANGUAGES.lookup(langtag) in self.__segments

    def __getitem__(self, langtag: LangT) -> Segment:
        ltag: LangTag = LANGUAGES.lookup(langtag)
        return self.__segments[ltag]

    def __setitem__(self, langtag: LangT, item: Segment) -> None:
        assert item.lang.tag == langtag
        self.append(item)

    def append(self, item: Segment) -> None:
        for atag in item.lang.aliases:
            self.__segments.setdefault(atag, item)
        self.__segments[item.lang.tag] = item

    def lookup(self, langtag: LangT) -> Segment:
        ltag: LangTag = LANGUAGES.lookup(langtag)
        if ltag in self.__segments:
            return self.__segments[ltag]
        for _tag in ltag.tags:
            ltag = LANGUAGES[_tag]
            if ltag in self.__segments:
                return self.__segments[ltag]
        raise LookupError(f"No such language tag: {langtag}")

    @classmethod
    def load(cls, path: str) -> "Message":
        instance = cls()
        for base in os.listdir(path):
            file: str = os.path.join(path, base)
            if os.path.isfile(file):
                segment: Segment = Segment.loadf(file)
                instance[segment.lang.tag] = segment
        return instance
