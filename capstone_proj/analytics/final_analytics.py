import pandas as pd
import os

def run_final_analytics(marks_csv="data/marks.csv", results_csv="data/student_results.csv"):
    """
    Merge marks + processed results, generate insights:
    - Top 3 students by Percentage
    - Average marks per subject (Maths, Python, ML) overall
    Returns: merged_df, top3_df, avg_marks_series
    """
    if not os.path.exists(marks_csv):
        raise FileNotFoundError(f"{marks_csv} not found")
    if not os.path.exists(results_csv):
        raise FileNotFoundError(f"{results_csv} not found")

    # Read CSVs
    df1 = pd.read_csv(marks_csv)       # StudentID, Maths, Python, ML
    df2 = pd.read_csv(results_csv)     # StudentID, Maths, Python, ML, TotalMarks, Percentage, Result

    # Merge on StudentID
    merged_df = pd.merge(df1, df2, on='StudentID', how='inner')

    # Keep only final marks
    merged_df = pd.merge(df1, df2, on='StudentID', how='inner', suffixes=('_original', '_final'))

# Keep only the final marks from student_results
    merged_df = merged_df[['StudentID', 'Maths_final', 'Python_final', 'ML_final', 'TotalMarks', 'Percentage', 'Result']]

# Top 3 students
    top3_df = merged_df.sort_values(by="Percentage", ascending=False).head(3)

# Average per subject
    avg_marks_series = merged_df[["Maths_final", "Python_final", "ML_final"]].mean().round(2)

    

    return merged_df, top3_df, avg_marks_series
