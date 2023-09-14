from downloader import S3Downloader
import time

s3downloader = S3Downloader()

start = time.time()
for _ in range(1):
    raw_histories = s3downloader.get_summaries_by_year(2022)
end = time.time()
duration = end - start
print(f"Temps d'exécution avec Threading total: {duration} secondes")
print(f"Nombre de fichiers avec Threading total: {len(raw_histories)}")


