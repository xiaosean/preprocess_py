import pandas as pd
import numpy as np


if __name__ == '__main__':
    # 讀取xlsx data frame 並秀出資料
    df = pd.read_excel("persona smaple data.xlsx")
    # print(df)

    # 列出欄位名稱
    # print(df.columns)

    # 秀出某一欄
    # print(df["黑糖"])

    # 最後依照某一列排序
    # df = df.sort(["total"], ascending=False)
    # print(df)
    print(df.columns)
    feature_cols = ['ACTV_TYPE', 'AGE', 'APPLY_CURR_EBILL_SBILL_FLAG', 'AUTOPAY_IND',
       'AVG_HS_USE_MONTH', 'BILL_CITY_NAME', 'CHURN_TYPE', 'CUST_TYPE']
    df = df[feature_cols]
    df['CHURN_TYPE'] = df['CHURN_TYPE'].apply(str)
    df['CHURN_TYPE'] = df['CHURN_TYPE'].replace({"nan" :"i'm empty", "test" : "revise_test"}, regex = True)
    print(df)
    df.to_excel("處理完成的.xlsx")

