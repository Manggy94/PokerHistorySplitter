from downloader import S3Downloader

s3downloader = S3Downloader()
summaries = s3downloader.summaries_list
histories = s3downloader.raw_histories_list
print(summaries[0])
