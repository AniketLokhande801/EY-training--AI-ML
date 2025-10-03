import pandas as pd
import numpy as np
# df = pd.DataFrame([1,2,3,4,5])
# print(df)

data = {
    "Name": ["Rahul", "Priya", "Arjun", "Neha", "Vikram"],
    "Age": [21, 22, 20, 23, 21],
    "Course": ["AI", "ML", "Data Science", "AI", "ML"],
    "Marks": [85, 90, 78, 88, 95]
}

df=pd.DataFrame(data)
# print(df)
# print(df["Name"])
# print(df.iloc[2])
# print(df.loc[2,"Marks"])


# #filter
# df1=df[df["Marks"]>85]
# print(df1)

df["result"]=np.where(df["Marks"]>85,"pass","fail")
print(df)
print("-----------------------------")

df.loc[df["Name"]=="Neha","Marks"]=92
print(df)