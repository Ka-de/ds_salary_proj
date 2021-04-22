from scraper import get_jobs

df = get_jobs("data scientist", 1000, False)
df.to_csv("glassdoor_jobs.csv", index=False)