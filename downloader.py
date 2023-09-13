import boto3
import os
from functools import cached_property

from dotenv import load_dotenv

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
        self.summaries = None
        self.raw_histories = None

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

    @cached_property
    def summaries_list(self) -> list:
        """
        Returns a list of all summaries in the bucket
        """
        return list(self.bucket.objects.filter(Prefix="data/summaries/"))

    def list_summaries_by_year(self, year) -> list:
        """
        Returns a list of all summaries in the bucket
        """
        return list(self.bucket.objects.filter(Prefix=f"data/summaries/{year}"))

    def list_summaries_by_month_of_year(self, year, month) -> list:
        """"""
        return list(self.bucket.objects.filter(Prefix=f"data/summaries/{year}/{month:02}"))

    @property
    def summaries_key_list(self) -> list:
        """
        Returns a list of all summaries keys in the bucket
        """
        return [s.key for s in self.summaries_list]

    @cached_property
    def get_summaries(self):
        """
        Returns a list of all summary objects in the bucket
        """
        return [s.get() for s in self.summaries_list]

    def get_summaries_by_year(self, year):
        """
        Returns a list of all summary objects in the bucket
        """
        return [s.get() for s in self.list_summaries_by_year(year)]

    def get_summaries_by_month_of_year(self, year, month):
        """
        Returns a list of all summary objects in the bucket
        """
        return [s.get() for s in self.list_summaries_by_month_of_year(year, month)]

    @property
    def raw_histories_list(self):
        """
        Returns a list of all raw histories in the bucket
        """
        return list(self.bucket.objects.filter(Prefix="data/histories/raw/"))

    def list_raw_history_keys(self):
        """
        Returns a list of all raw histories keys in the bucket
        """
        return [h.key for h in self.raw_histories_list]

    def get_raw_histories(self, bucket_name: str = "manggy-poker"):
        """
        Returns a list of all raw history objects in the bucket
        """
        bucket = self.s3.Bucket(bucket_name)
        pseudo_histories = bucket.objects.filter(Prefix="data/histories/raw/")
        histories = [h.get() for h in pseudo_histories]
        return list(histories)

    def load_raw_histories(self):
        """
        Loads all raw history objects into memory
        :return: 
        """
        self.raw_histories = self.get_raw_histories()

    def load_summaries(self):
        """
        Loads all summary objects into memory
        :return: 
        """
        self.summaries = self.get_summaries()
