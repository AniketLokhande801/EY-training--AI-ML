import pandas as pd

df=pd.read_csv("student.csv")

# print(df.head())

df.dropna(inplace=True)
df["Marks"]=df["Marks"].astype(int)
df["Result"]=df["Marks"].apply(lambda x: "pass" if x > 50 else "fail")


df.to_csv("cleaned_student_index_TRUE.csv",index=True)
df.to_csv("cleaned_student_index_False.csv",index=False)


