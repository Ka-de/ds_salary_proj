from scraper import get_jobs

df = get_jobs("data scientist", 40, False)
print(df)