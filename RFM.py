import datetime as dt
import pandas as pd
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.float_format', lambda x: '%.5f' % x)

df_ = pd.read_excel(r"...\online_retail_II.xlsx", sheet_name="Year 2010-2011")

df = df_.copy()

df.describe().T

df.isnull().values.any()

df.isnull().sum()

df.dropna(inplace=True)

df['Description'].nunique()

df['Description'].value_counts().head()

df.groupby('Description')['Quantity'].sum().sort_values(ascending=False).head()

df = df[~df['Invoice'].str.contains('C', na=False)]

df["TotalPrice"] = df["Quantity"] * df["Price"]

today_date = dt.datetime(2011, 12, 11)

rfm = df.groupby('Customer ID').agg({'InvoiceDate': lambda x: (today_date - x.max()).days,
                                     'Invoice': lambda x: x.nunique(),
                                     'TotalPrice': lambda x: x.sum()})

rfm.columns = ['recency', 'frequency', 'monetary']

rfm = rfm[(rfm['monetary'] > 0)]

rfm["recency_score"] = pd.qcut(rfm['recency'], 5, labels=[5, 4, 3, 2, 1])

rfm["freqency_score"] = pd.qcut(rfm['frequency'].rank(method="first"), 5, labels=[1, 2, 3, 4, 5])

rfm["monetary_score"] = pd.qcut(rfm['monetary'], 5, labels=[1, 2, 3, 4, 5])

rfm['RFM_SCORE'] = (rfm['recency_score'].astype(str) + rfm['freqency_score'].astype(str))

seg_map = {
    r'[1-2][1-2]': 'hibernating',
    r'[1-2][3-4]': 'at_risk',
    r'[1-2]5': 'cant_lose',
    r'3[1-2]': 'about_to_sleep',
    r'33': 'need_attention',
    r'[3-4][4-5]': 'loyal_customers',
    r'41': 'promising',
    r'51': 'new_customers',
    r'[4-5][2-3]': 'potential_loyalists',
    r'5[4-5]': 'champions'
}

rfm['segment'] = rfm['RFM_SCORE'].replace(seg_map, regex=True)

rfm[["segment", "recency", "frequency", "monetary"]].groupby("segment").agg(["mean", "count"])

new_df = pd.DataFrame()

new_df["loyal_customer_id"] = rfm[rfm["segment"] == "loyal_customers"].index

new_df.to_excel("loyal_customers.xlsx")
