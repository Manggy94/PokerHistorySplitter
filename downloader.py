import queue

import boto3
import os
import threading
from dotenv import load_dotenv
from functools import cached_property

load_dotenv()


class S3Downloader:
    """
    A class to download Hand history files from S3 bucket
    """

    def __init__(self):
        self.s3 = boto3.resource(
            's3',
            region_name=os.environ.get("DO_REGION"),
            endpoint_url=os.environ.get("DO_ENDPOINT"),
            aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY")
        )
        self.bucket = self.s3.Bucket("manggy-poker")

    @cached_property
    def objects_iterator(self):
        """
        Returns an iterator over all objects in the bucket
        """
        return self.bucket.objects.all()

    @cached_property
    def list_objects(self):
        """
        Returns a list of all objects in the bucket
        """
        return list(self.objects_iterator)

    def get_object(self, key):
        """
        Returns an object from the bucket
        """
        return self.bucket.Object(key).get()

    def threaded_get_object(self, key, result_queue):
        result = self.get_object(key)
        result_queue.put(result)

    @cached_property
    def summaries_list(self) -> list:
        """
        Returns a list of all summaries in the bucket
        """
        return list(self.bucket.objects.filter(Prefix="data/summaries/"))

    @property
    def summaries_key_list(self) -> list:
        """
        Returns a list of all summaries keys in the bucket
        """
        return [s.key for s in self.summaries_list]

    def list_summaries_by_year(self, year) -> list:
        """
        Returns a list of all summaries in the bucket
        """
        return list(self.bucket.objects.filter(Prefix=f"data/summaries/{year}"))

    def list_summaries_keys_by_year(self, year):
        """
        Returns a list of  summary objects in the bucket for a certain year
        """
        return [s.key for s in self.list_summaries_by_year(year)]

    def list_summaries_by_month_of_year(self, year, month) -> list:
        """"""
        return list(self.bucket.objects.filter(Prefix=f"data/summaries/{year}/{month:02}"))

    def list_summaries_keys_by_year_of_month(self, year, month):
        """
        Returns a list of  summary objects in the bucket for a certain year
        """
        return [s.key for s in self.list_summaries_by_year_of_month(year, month)]


    @cached_property
    def get_summaries(self):
        """
        Returns a list of all summary objects in the bucket
        """
        threads = []
        result_queue = queue.Queue()
        for key in self.summaries_key_list:
            thread = threading.Thread(target=self.threaded_get_object, args=(key, result_queue))
            thread.start()
            threads.append(thread)
        for thread in threads:
            thread.join()
        summaries = []
        while not result_queue.empty():
            summaries.append(result_queue.get())
        return summaries
    def get_summaries_by_year(self, year):
        """
        Returns a list of all summary objects in the bucket
        """
        threads = []
        result_queue = queue.Queue()
        for key in self.list_summaries_keys_by_year(year):
            thread = threading.Thread(target=self.threaded_get_object, args=(key, result_queue))
            thread.start()
            threads.append(thread)
        for thread in threads:
            thread.join()
        summaries = []
        while not result_queue.empty():
            summaries.append(result_queue.get())
        return summaries

    def get_summaries_by_month_of_year(self, year, month):
        """
        Returns a list of all summary objects in the bucket
        """
        threads = []
        result_queue = queue.Queue()
        for key in self.list_summaries_keys_by_year_of_month(year, month):
            thread = threading.Thread(target=self.threaded_get_object, args=(key, result_queue))
            thread.start()
            threads.append(thread)
        for thread in threads:
            thread.join()
        summaries = []
        while not result_queue.empty():
            summaries.append(result_queue.get())
        return summaries

    @cached_property
    def raw_histories_list(self):
        """
        Returns a list of all raw histories in the bucket
        """
        return list(self.bucket.objects.filter(Prefix="data/histories/raw/"))

    def list_raw_histories_by_year(self, year) -> list:
        """
        Returns a list of all histories in the bucket
        """
        return list(self.bucket.objects.filter(Prefix=f"data/histories/raw/{year}"))

    def list_raw_histories_keys_by_year(self, year):
        """
        Returns a list of  raw history objects in the bucket for a certain year
        """
        return [h.key for h in self.list_raw_histories_by_year(year)]

    def list_raw_histories_by_month_of_year(self, year, month) -> list:
        """"""
        return list(self.bucket.objects.filter(Prefix=f"data/histories/raw/{year}/{month:02}"))

    def list_raw_histories_keys_by_month_of_year(self, year, month):
        """
        Returns a list of  raw history objects in the bucket for a certain year
        """
        return [h.key for h in self.list_raw_histories_by_month_of_year(year, month)]

    @cached_property
    def raw_histories_keys_list(self):
        """
        Returns a list of all raw histories keys in the bucket
        """
        return [h.key for h in self.raw_histories_list]

    @cached_property
    def get_raw_histories(self):
        """
        Returns a list of all raw history objects in the bucket
        """
        threads = []
        result_queue = queue.Queue()
        for key in self.raw_histories_keys_list:
            thread = threading.Thread(target=self.threaded_get_object, args=(key, result_queue))
            thread.start()
            threads.append(thread)
        for thread in threads:
            thread.join()
        raw_histories = []
        while not result_queue.empty():
            raw_histories.append(result_queue.get())
        return raw_histories



    def get_raw_histories_by_year(self, year):
        threads = []
        result_queue = queue.Queue()
        for key in self.list_raw_histories_keys_by_year(year):
            thread = threading.Thread(target=self.threaded_get_object, args=(key, result_queue))
            thread.start()
            threads.append(thread)
        for thread in threads:
            thread.join()
        raw_histories = []
        while not result_queue.empty():
            raw_histories.append(result_queue.get())
        return raw_histories

    def get_raw_histories_by_month_of_year(self, year, month):
        """
        Returns a list of  raw history objects in the bucket for a certain month of year
        """
        threads = []
        result_queue = queue.Queue()
        for key in self.list_raw_histories_keys_by_month_of_year(year, month):
            thread = threading.Thread(target=self.threaded_get_object, args=(key, result_queue))
            thread.start()
            threads.append(thread)
        for thread in threads:
            thread.join()
        raw_histories = []
        while not result_queue.empty():
            raw_histories.append(result_queue.get())
        return raw_histories

    def threaded_get_raw_histories_by_month_of_year(self, year, month, result_queue):
        result = self.get_raw_histories_by_month_of_year(year, month)
        result_queue.put(result)
