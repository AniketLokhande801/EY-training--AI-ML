import pandas as pd
from datetime import datetime
import logging
import os

def run_etl(input_csv: str, output_prefix: str = "student_results"):
    """
    Reads CSV, calculates total, percentage, result, saves processed CSV.
    Returns: (output_file_path, dataframe)
    """
    try:
        if not os.path.exists(input_csv):
            logging.error(f"ETL: Input file {input_csv} not found")
            raise FileNotFoundError(f"{input_csv} not found")
        
        df = pd.read_csv(input_csv)
        df["TotalMarks"] = df["Maths"] + df["Python"] + df["ML"]
        df["Percentage"] = round(df["TotalMarks"] / 3, 2)
        df["Result"] = df["Percentage"].apply(lambda x: "Pass" if x >= 50 else "Fail")
        
        # Save output with timestamp
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"data/{output_prefix}_{ts}.csv"
        df.to_csv(output_file, index=False)
        logging.info(f"ETL: Processed CSV saved to {output_file}")
        
        return output_file, df

    except Exception as e:
        logging.error(f"ETL: Error processing {input_csv} - {e}", exc_info=True)
        raise e
