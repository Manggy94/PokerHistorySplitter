import re


class FileSplitter:
    """
    Class that splits a Winamax Poker hand HistoryHistory file into multiple handhistory txt files.
    """
    def __init__(self):

        self._split_re = re.compile(r"\*\*\*\s+\n?|\n\n+")
        self._winamax_new_hand_re = re.compile(r"Winamax\s+Poker")

    def split_raw_file(self, hh_text: str):
        """
        Splits a raw history file into an array of raw hands
        :param hh_text: raw text for entire tournament/session
        :return: array of different hands played
        """
        raw_hands = re.split(self._winamax_new_hand_re, hh_text)
        raw_hands.pop(0)
        return raw_hands

