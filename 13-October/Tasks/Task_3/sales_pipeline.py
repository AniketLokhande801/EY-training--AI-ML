import pandas as pd
import datetime as dt
def main():
    # load
    p_df=pd.read_csv("products.csv")
    c_df=pd.read_csv("customers.csv")
    o_df=pd.read_csv("orders.csv")

    # Transform
    df_product_order=pd.merge(o_df,c_df,how="inner",on="CustomerID")
    merged_df=pd.merge(df_product_order,p_df,how="inner",on="ProductID")

    merged_df["TotalAmount"]=merged_df["Quantity"]*merged_df["Price"]
    merged_df["OrderDate"]=pd.to_datetime(merged_df["OrderDate"])
    merged_df["OrderMonth"]=merged_df["OrderDate"].dt.month

    filtered_df=merged_df[(merged_df["Quantity"]>=2) & (merged_df["Country"].isin(["India","UAE"]))]

    total_revenue_by_category=filtered_df.groupby("Category")["TotalAmount"].sum().reset_index()

    total_revenue_by_customer_segment= filtered_df.groupby("Segment")["TotalAmount"].sum().reset_index()

    filtered_df.sort_values(by="TotalAmount",ascending=False)

    # Load
    filtered_df.to_csv("processed_orders.csv",index=False)
    total_revenue_by_category.to_csv("category_summary.csv",index=False)
    total_revenue_by_customer_segment.to_csv("segment_summary.csv",index=False)


if __name__ == "__main__":
    main()