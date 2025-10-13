import pandas as pd

def age_group(age):
    if age < 30:
        return "Young"
    elif age < 50:
        return "Adult"
    else:
        return "Senior"

def main():
    df = pd.read_csv("customer.csv")

    df["Age_group"]=df["Age"].apply(age_group)

    # filter age less than 20
    df1=df[df["Age"]>=20]

    print(df1)
    df1.to_csv("filtered_customers.csv",index=False)

if __name__ == "__main__":
    main()
