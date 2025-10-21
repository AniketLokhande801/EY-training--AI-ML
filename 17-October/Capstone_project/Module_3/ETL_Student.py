import pandas as pd
import numpy as np
import datetime as dt
def run_etl(filepath):
    start=dt.datetime.now()
    df= pd.read_csv(filepath)
    print(f"extracted data from marks.csv at - {dt.datetime.now()} ")
    print(df.head())

    df["TotalMarks"]=df["Maths"]+df["Python"]+df["ML"]
    df["Percentage"]=round((df["TotalMarks"]/300)*100,2)
    df["Result"] = df["Percentage"].apply(lambda x: "Pass" if x >= 50 else "Fail")
    print(f"Transformation done on data added columns:- Totalmarks,Percentage,Result at - {dt.datetime.now()} ")

    df.to_csv("student_results.csv", index=False)
    end=dt.datetime.now()
    print(f"transformed data loaded at student_results.csv at -  {dt.datetime.now()} ")
    print(f"ETL RUN COMPLETED! at - {dt.datetime.now()}")
    print(f"time required for etl - {end-start} ")
    return df
run_etl("marks.csv")

