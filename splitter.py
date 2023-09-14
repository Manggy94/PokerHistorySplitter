import re
from downloader import S3Downloader


class FileSplitter:
    """
    Class that splits a Winamax Poker hand HistoryHistory file into multiple handhistory txt files.
    """
    def __init__(self):
        self._split_re = re.compile(r"\*\*\*\s+\n?|\n\n+")
        self._winamax_new_hand_re = re.compile(r"Winamax\s+Poker")
        self.downloader = S3Downloader()

    def get_text(self, object_summary):
        """
        Returns the text of a raw hand history or summary file
        :param object_summary: S3 object summary
        :return: text of hand history file or summary file
        """
        return object_summary.get().get('Body').read().decode('utf-8')

    def split_raw_file(self, hh_text: str):
        """
        Splits a raw history file into an array of raw hands
        :param hh_text: raw text for entire tournament/session
        :return: array of different hands played
        """
        raw_hands = re.split(self._winamax_new_hand_re, hh_text)
        raw_hands.pop(0)
        return raw_hands


