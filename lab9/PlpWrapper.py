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

    def get_noun_ids(self, word):
        return [clp_id for clp_id in self.plp.rec(word) if self.pos(clp_id) == PartOfSpeech.RZECZOWNIK]

    def get_preposition(self, word):
        for pos in self.part_of_speech(word):
            if pos == PartOfSpeech.PRZYIMEK:
                return pos
        return None

    def parts_of_grammar(self, word, word_id):
        vec = self.plp.vec(word_id, word)
        return list(set([PartOfSpeech((i - 1) % 7 + 1) for i in vec]))

    def part_of_speech(self, word):
        parts = list()
        for id in self.plp.rec(word):
            parts.append(self.pos(id))
        return parts

    def pos(self, id):
        return PartOfSpeech(self.plp.CLPLIB.clp_pos(c_int(id)))

    def grammar_case(self, word, word_id):
        vec = self.plp.vec(word_id, word)
        return list(set([GrammarCase((i - 1) % 7 + 1) for i in vec]))

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

    def str_map(self):
        return {
            0: "???",
            1: "RZECZOWNIK",
            2: "CZASOWNIK",
            3: "PRZYMIOTNIK",
            4: "LICZEBNIK",
            5: "ZAIMEK",
            6: "PRZYSLOWEK",
            7: "WYKRZYNIK",
            8: "PRZYIMEK",
            9: "SPOJNIK",
            10: "NIEODMIENNY",
            11: "SKROT"
        }

    def __str__(self):
        return self.str_map()[self.value]


class GrammarCase(Enum):
    MIANOWNIK = 1
    DOPELNIACZ = 2
    CELOWNIK = 3
    BIERNIK = 4
    NARZEDNIK = 5
    MIEJSCOWNIK = 6
    WOLACZ = 7
    MIANOWNIK_MN = 8
    DOPELNIACZ_MN = 9
    CELOWNIK_MN = 10
    BIERNIK_MN = 11
    NARZEDNIK_MN = 12
    MIEJSCOWNIK_MN = 13
    WOLACZ_MN = 14

    def str_map(self):
        return {
            1: "MIANOWNIK",
            2: "DOPELNIACZ",
            3: "CELOWNIK",
            4: "BIERNIK",
            5: "NARZEDNIK",
            6: "MIEJSCOWNIK",
            7: "WOLACZ"
        }

    def __str__(self):
        return self.str_map()[(self.value - 1) % 7 + 1]
