import re
from pkrhistorysplitter.downloader import S3Downloader, threading
from io import BytesIO
import datetime


class FileSplitter:
    """
    Class that splits a Winamax Poker hand HistoryHistory file into multiple handhistory txt files.
    """
    def __init__(self):
        self._split_re = re.compile(r"\*\*\*\s+\n?|\n\n+")
        self._winamax_new_hand_re = re.compile(r"Winamax\s+Poker\s+-")
        self._hand_id_re = re.compile(r"-\s+HandId:\s+#(?P<hand_id>[0-9-]+)\s+-\s+(?P<Variant>[A-Za-z ]+)\s+")

        self.downloader = S3Downloader()

    def get_text(self, object_summary):
        """
        Returns the text of a raw hand history or summary file
        :param object_summary: S3 object summary
        :return: text of hand history file or summary file
        """
        return object_summary.get('Body').read().decode('utf-8')

    def split_raw_file(self, hh_text: str):
        """
        Splits a raw history file into an array of raw hands
        :param hh_text: raw text for entire tournament/session
        :return: array of different hands played
        """
        raw_hands = re.split(self._winamax_new_hand_re, hh_text)
        raw_hands.pop(0)
        return raw_hands

    def separate_hands(self, raw_hands: list, path_prefix: str):
        """
        Separates the hands into different files
        """
        try:
            threads = []
            id_list = [self.get_hand_id(rh) for rh in raw_hands]
            io_hands = [BytesIO(rh.encode('utf-8')) for rh in raw_hands]
            for i in range(len(raw_hands)):
                hand_id = id_list[i]
                io_hand = io_hands[i]
                path = f"{path_prefix}/{hand_id}.txt"
                thread = threading.Thread(target=self.downloader.bucket.upload_fileobj, args=(io_hand, path))
                thread.start()
                threads.append(thread)
            for thread in threads:
                thread.join()
        except AttributeError:
            raise AttributeError




    def get_hand_id(self, hand: str):
        """
        Gets the hand id from a hand txt in list of hands
        :param hand:  hand text
        :return: hand id
        """
        try:
            r = re.search(self._hand_id_re, hand).group("hand_id")
            return r.strip()
        except AttributeError:
            print(hand)
            raise AttributeError

    def divide_raw_history_file(self, history_object):
        """
        Divides a raw history file into separate hand history files and uploads them to the bucket
        """
        try:
            year = history_object.get("Metadata").get("year")
            month = history_object.get("Metadata").get("month")
            day = history_object.get("Metadata").get("day")
            tournament_id = history_object.get("Metadata").get("tournament-id")
            prefix_path = f"data/histories/split/{year}/{month}/{day}/{tournament_id}"
            raw_txt = self.get_text(history_object)
            hands_raw_list = self.split_raw_file(raw_txt)
            self.separate_hands(hands_raw_list, prefix_path)
        except AttributeError:
            tournament_id = history_object.get("Metadata").get("tournament-id")
            print(f"Probleme de type Attribute Error sur le tournoi main {tournament_id}")
            pass

    def divide_raw_history_files(self, history_objects):
        """
        Divides a list of raw history files into separate hand history files and uploads them to the bucket
        """
        for history_object in history_objects:
            self.divide_raw_history_file(history_object)


    def divide_all_raw_history_files(self):
        """
        Divides all raw history files into separate hand history files and uploads them to the bucket
        """
        for year in range(2015, datetime.date.today().year + 1):
            print(f"Dividing raw history files for year {year}")
            raw_histories = self.downloader.get_raw_histories_by_year(year)
            self.divide_raw_history_files(raw_histories)
