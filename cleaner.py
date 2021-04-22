import pandas as pd

df = pd.read_csv("glassdoor_jobs.csv")

#salary cleaning
df = df[df["salary"] != "nan"]


#job stack
#state
#size
#age
#revenue cleaning
