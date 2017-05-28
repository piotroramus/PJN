from plp import PLP
from enum import Enum

from ctypes import c_int


class PlpWrapper(object):
    def __init__(self):
        self.plp = PLP()

    def get_nouns(self, word):
        nouns = list()
        for pos in self.part_of_speech(word):
            if pos == PartOfSpeech.RZECZOWNIK:
                nouns.append(pos)
        return nouns

    def get_preposition(self, word):
        for pos in self.part_of_speech(word):
            if pos == PartOfSpeech.PRZYIMEK:
                return pos
        return None

    def part_of_speech(self, word):
        parts = list()
        for id in self.plp.rec(word):
            parts.append(self.pos(id))
        return parts

    def pos(self, id):
        return PartOfSpeech(self.plp.CLPLIB.clp_pos(c_int(id)))


class PartOfSpeech(Enum):
    UNKNOWN = 0
    RZECZOWNIK = 1
    CZASOWNIK = 2
    PRZYMIOTNIK = 3
    LICZEBNIK = 4
    ZAIMEK = 5
    PRZYSLOWEK = 6
    WYKRZYKNIK = 7
    PRZYIMEK = 8
    SPOJNIK = 9
    NIEODMIENNY = 10
    SKROT = 11
