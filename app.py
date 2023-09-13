from downloader import S3Downloader
import time

s3downloader = S3Downloader()
start = time.time()
histories = s3downloader.get_raw_histories_by_month_of_year(2021, 1)
end = time.time()
duration = end - start
print(f"Temps d'exécution: {duration} secondes")
print(histories)
