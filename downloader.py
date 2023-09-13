import boto3
import os

from dotenv import load_dotenv

load_dotenv()


class S3Downloader:
    """
    A class to download Hand history files from S3 bucket
    """

    def __init__(self):
        self.summaries = None
        self.raw_histories = None
        self.s3 = boto3.resource(
            's3',
            region_name=os.environ.get("DO_REGION"),
            endpoint_url=os.environ.get("DO_ENDPOINT"),
            aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY")
        )
        self.raw_histories_list = self.list_raw_history_keys()
        self.summaries_list = self.list_summary_keys()

    def objects_iterator(self, bucket_name: str = "manggy-poker"):
        """
        Returns an iterator over all objects in the bucket
        """
        bucket = self.s3.Bucket(bucket_name)
        return bucket.objects.all()

    def list_objects(self, bucket_name: str = "manggy-poker"):
        """
        Returns a list of all objects in the bucket
        """
        it = self.objects_iterator(bucket_name)
        return list(it)

    def list_summaries(self, bucket_name: str = "manggy-poker"):
        """
        Returns a list of all summaries in the bucket
        """
        bucket = self.s3.Bucket(bucket_name)
        summ = bucket.objects.filter(Prefix="data/summaries/")
        return list(summ)

    def list_summary_keys(self, bucket_name: str = "manggy-poker"):
        """
        Returns a list of all summaries keys in the bucket
        """
        summ = self.list_summaries(bucket_name)
        return [s.key for s in summ]

    def get_summaries(self, bucket_name: str = "manggy-poker"):
        """
        Returns a list of all summary objects in the bucket
        """
        bucket = self.s3.Bucket(bucket_name)
        pseudo_summaries = bucket.objects.filter(Prefix="data/summaries/")
        summ = [s.get() for s in pseudo_summaries]
        return list(summ)

    def list_raw_histories(self, bucket_name: str = "manggy-poker"):
        """
        Returns a list of all raw histories in the bucket
        """
        bucket = self.s3.Bucket(bucket_name)
        hist = bucket.objects.filter(Prefix="data/histories/raw/")
        return list(hist)

    def list_raw_history_keys(self, bucket_name: str = "manggy-poker"):
        """
        Returns a list of all raw histories keys in the bucket
        """
        hist = self.list_raw_histories(bucket_name)
        return [h.key for h in hist]

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
