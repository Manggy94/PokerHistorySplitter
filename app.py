from downloader import S3Downloader
import time

s3downloader = S3Downloader()
start = time.time()
for _ in range(2):
    s3downloader.get_summaries_by_month_of_year(2023, 8)
end = time.time()
duration = end - start
print(f"Temps d'exécution: {duration} secondes")
