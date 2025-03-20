# from bullscatch_backtest.spot_fetch_spa import get_spot_data
# # Spot Data Fetch
# data = get_spot_data("2024-10-25", "nifty")
# print(data)

# from bullscatch_backtest.expiry_list_spa import get_expiries

# expiries = get_expiries("nifty", "options", "2024-01-25")
# print(expiries)

##########################Single Date Option Chain Fetch################################

# from bullscatch_backtest.option_chain_spa import get_option_chain
# # option_chain_df = get_option_chain("date(YYYY-MM-DD)", "Expiry(YYYY_MM_DD)","nifty")
# option_chain_df = get_option_chain("2025-02-28", "2025_03_06","nifty")
# print(option_chain_df)

# # Assuming option_chain_df is already defined
# filtered_df = option_chain_df[option_chain_df['strike'] == 22450]

# # Display the filtered rows
# print(filtered_df)

########################## Multiple Date Option Chain Fetch For Multiple Expiry Fetch################################

# from multidate_option_chain_spa import OptionDataFetcher
# import time
# # Define date-expiry pairs
# date_expiry_pairs = [
#     ("2019_10_01", "2019_10_03"),
#     ("2019_10_02", "2019_10_03"),
#     ("2019_10_03", "2019_10_03"),
#     ("2019_10_08", "2019_10_10"),
#     ("2019_10_15", "2019_10_17"),
#     ("2019_10_22", "2019_10_24"),
#     ("2019_10_29", "2019_10_31")
# ]

# # Create fetcher instance
# fetcher = OptionDataFetcher()

# # Fetch data
# start_time = time.time()
# fetched_data = fetcher.fetch_all_data(date_expiry_pairs)
# print(f"\nFetched {len(fetched_data)} records in {time.time() - start_time:.2f} seconds")

# # Print results
# for key, value in fetched_data.items():
#     print(f"{key}: {value}")

########################## Processed Option Chain ################################

# from bullscatch_backtest.processed_option_chain_spa import fetch_and_process_option_chain

# # Fetch and process data
# final_option_chain_df = fetch_and_process_option_chain("2025-02-28", "2025_03_06", "nifty")

# # Display processed DataFrame
# print(final_option_chain_df)

# # Example: Filter by strike price
# filtered_df = final_option_chain_df[final_option_chain_df['strike'] == 22850]
# print(filtered_df)

# # Example: Filter by timestamp range
# start_time = "2025-02-28 09:15:01"
# end_time = "2025-02-28 09:24:00"
# timestamp_filtered_df = filtered_df[(filtered_df['timestamp'] >= start_time) &  
#                                     (filtered_df['timestamp'] <= end_time)]
# print(timestamp_filtered_df.head(20))


##########################  Option Chain ATM ################################
# from bullscatch_backtest.processed_option_chain_spa import option_chain_atm
# # Call function with desired values
# filtered_df = option_chain_atm("2024-07-10", "2024_07_11", "nifty", 22400)

# # Display the filtered DataFrame
# print(filtered_df)

# unique_strikes = sorted(filtered_df['strike'].unique())

# # Display the unique strikes
# print(unique_strikes)

# strike_value = 22450
# option_type_value = "CE"

# filtered_strike_df = filtered_df[(filtered_df['strike'] == strike_value) & 
#                                  (filtered_df['option_type'] == option_type_value)]

# print(f"\nData for Strike = {strike_value} and Option Type = {option_type_value}:\n")
# print(filtered_strike_df.head(50))

##########################  Expiry List ################################

# from bullscatch_backtest.expiry_list_spa import get_expiries

# expiries = get_expiries("nifty", "options", "2024-03-03")
# print(expiries)
