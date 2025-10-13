import pandas as pd
from datetime import datetime
def main():
    df = pd.read_csv("inventory.csv")
    df["RestockNeeded"]=df.apply(lambda x: "Yes" if x["Quantity"]> x["ReorderLevel"] else "No",axis=1)
    # TotalValue = Quantity * PricePerUnit
    df["TotalValue"]=df["Quantity"]*df["PricePerUnit"]

    df.to_csv("restock_report.csv",index=False)
    print(df)
    print(f"Pipeline completed and report saved at{datetime.now()}")
if __name__ == "__main__":
    main()