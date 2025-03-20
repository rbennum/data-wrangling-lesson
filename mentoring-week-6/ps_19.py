import pandas as pd

def single_rfm(rfm_data, on_column, labels):
    quantiles = rfm_data[on_column].quantile([0.2, 0.4, 0.6, 0.8]).tolist()
    sorted_col = pd.cut(
        rfm_data[on_column],
        bins=[-float("inf")]+quantiles+[float("inf")],
        labels=labels
    ).astype(int)
    return sorted_col

def calculate_rfm_score(rfm_data: pd.DataFrame) -> pd.DataFrame:
    rfm_data['Score_Recency'] = single_rfm(rfm_data, 'Recency', [5, 4, 3, 2, 1])
    rfm_data['Score_Frequency'] = single_rfm(rfm_data, 'Frequency', [1,2,3,4,5])
    rfm_data['Score_Monetary'] = single_rfm(rfm_data, 'Monetary', [1,2,3,4,5])
    
    rfm_data['Score_RFM'] = (
        rfm_data[['Score_Recency','Score_Frequency','Score_Monetary']].mean(axis=1)
    ).round(2)
    
    # sort values
    rfm_data.sort_values(
        by=['Score_RFM', 'Customer_ID'],
        ascending=[False, True],
        inplace=True
    )
    
    # remove score columns
    rfm_data.drop(columns=['Score_Recency', 'Score_Frequency', 'Score_Monetary'], inplace=True)

    return rfm_data

# Load the dataset
pd.set_option('display.max_columns', None)
rfm_df = pd.read_csv('customer_transactions_rfm.csv')

# Calculate RFM scores
rfm_result = calculate_rfm_score(rfm_data=rfm_df)

# Display mininum and maximum Score RFM
print(f"Minimum Score RFM: {rfm_result['Score_RFM'].min()}")
print(f"Maximum Score RFM: {rfm_result['Score_RFM'].max()}\n")

# Display the RFM DataFrame with scores
print(rfm_result)