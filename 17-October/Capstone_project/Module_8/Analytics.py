import pandas as pd
import numpy as np

df1=pd.read_csv("students.csv")

df2=pd.read_csv("student_results.csv")


merged_df = pd.merge(df1, df2, on='StudentID', how='inner')

print("Merged DataFrame:")
print(merged_df.head())


top_3_students = merged_df.sort_values(by='Percentage', ascending=False).head(3)
print("\nTop 3 students by percentage:")
print(top_3_students[['StudentID', 'Maths', 'Python', 'ML', 'Percentage', 'Result']])


avg_marks = merged_df[['Maths', 'Python', 'ML']].mean()
print("\nAverage marks per course:")
print(avg_marks)
