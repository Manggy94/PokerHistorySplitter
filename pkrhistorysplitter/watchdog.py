import datetime
import time
from pkrhistorysplitter.splitter import FileSplitter


class S3Watchdog:
    """
    A class to watch a bucket for new files
    """

    def __init__(self,  interval: int = 10):
        """
        :param interval: interval between checks in seconds
        """
        self.interval = interval
        self.file_splitter = FileSplitter()
        self.downloader = self.file_splitter.downloader
        self.bucket = self.downloader.bucket
        date = datetime.datetime.now()
        self.prefix = f"data/histories/raw/{date.year}/{date.month}/{date.day}"
        self.file_splitter.divide_today_history_files()
        today_histories = self.downloader.list_today_raw_histories()
        self.registered_histories = [{"key": obj.key, "last_modified": obj.last_modified} for obj in today_histories]
        self.watch_condition = True
        print(f"Found {len(today_histories)} histories for today")

    def get_current_histories(self) -> list:
        """
        Gets the current histories in the bucket
        """
        today_histories = self.downloader.list_today_raw_histories()
        current_histories = [{"key": obj.key, "last_modified": obj.last_modified} for obj in today_histories]
        return current_histories

    def watch(self):
        """
        Watch the bucket for new files or files that have been modified
        """
        current_histories = self.get_current_histories()
        for history in current_histories:
            if history not in self.registered_histories:
                print(f"History at {history.get('key')} has been created or modified since last check")
                self.registered_histories.append(history)
                self.file_splitter.divide_raw_history_file(history)
            else:
                print(f"History at {history.get('key')} has not been modified")
        self.registered_histories = current_histories

    def stop(self):
        """
        Stops the watch
        """
        self.watch_condition = False

    def start(self):
        """
        Starts the watch
        """
        start_time = datetime.datetime.now()
        try:
            while self.watch_condition:
                self.watch()
                if (datetime.datetime.now() - start_time).seconds > 43200:
                    print("Watched for 12 hours, stopping")
                    self.stop()
                time.sleep(self.interval)
        except KeyboardInterrupt:
            print("Stop watching")

