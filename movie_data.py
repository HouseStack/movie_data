# import the necessary libraries
from pytrends.request import TrendReq
import csv
import pandas as pd
import time
from datetime import datetime, timedelta

# create a list of movie_ids
with open('USA_movies_post2003.csv', newline='') as csvfile:
    reader = csv.reader(csvfile)
    # skip the first row of the CSV file
    next(reader)
    # create a list of movie IDs from the remaining rows
    movie_ids = [row[0] for row in reader]
# create a test list of movie IDs
test_ids = movie_ids[:10]

# create a DataFrame to store the regional interest data for all movie_ids for all time
v1_df = pd.DataFrame()
# # create a DataFrame to store the regional interest data for all movie_ids for +1/-1 years around peak
# v2_df = pd.DataFrame()
# # create a DataFrame to store the peak dates for all movie_ids
# v3_df = pd.DataFrame()

# create a loss counter
l_count = 0
# set total equal to len() of your input list
total = len(movie_ids)

### START OF LOOP ###

for movie_id in movie_ids:
    # create pytrends object
    pytrends = TrendReq(hl='en-US', tz=360)
    suggestions = pytrends.suggestions(keyword=movie_id)
    # check if suggestions do not exist
    if not suggestions:
        print("No suggestions for " + movie_id)
        l_count += 1
        time.sleep(1)
        continue

    # get the first suggestion
    first_suggestion = suggestions[0]
    # extract the relevant information
    title = first_suggestion["title"]
    typ = first_suggestion["type"]
    mid = first_suggestion["mid"]
    name = title + " (" + typ + ")"
    # set up the search parameters
    kw_list = [mid]
    timeframe = "all"
    geo = "US"
    # build payload
    pytrends.build_payload(kw_list, timeframe=timeframe, geo=geo)
    # print statement
    print(name + " first request complete.")
    # delay for 1 second between requests
    time.sleep(1)

    # get regional interest data
    df = pytrends.interest_by_region(resolution="DMA")
    # check if there is not enough data
    if len(df[df.iloc[:, 0] == 100]) == 0:
        print("Not enough data for " + name)
        l_count += 1
        time.sleep(1)
        continue
    # rename column[0] to movie_id
    df = df.rename(columns={df.columns[0]: movie_id})
    # append df to v1_df
    v1_df = pd.concat([v1_df, df], axis=1)
    # print statement
    print(name + " second request complete.")
    # Delay for 1 second between requests
    time.sleep(1)

    # # get peak year
    # time_df = pytrends.interest_over_time()
    # peak = time_df[time_df.iloc[:, 0] == 100].index[0]
    # minus_one = peak.replace(year=peak.year - 1).strftime("%Y-%m-%d")
    # plus_one = peak.replace(year=peak.year + 1).strftime("%Y-%m-%d")
    # peak = peak.strftime("%Y-%m-%d")
    # # check if minus_one is earlier than "2004-01-01"
    # if minus_one < "2004-01-01":
    #     minus_one = "2004-01-01"
    # # get the first day of the present month
    # present_month = datetime.now().replace(day=1)
    # # check if plus_one is greater than the first day of the present month
    # if plus_one > present_month.strftime("%Y-%m-%d"):
    #     plus_one = present_month.strftime("%Y-%m-%d")
    # # redefine timeframe
    # timeframe = minus_one + " " + plus_one
    # # build new payload
    # pytrends.build_payload(kw_list, timeframe=timeframe, geo=geo)
    # # print statement
    # print(name + " third request complete.")
    # # delay for 1 second between requests
    # time.sleep(1)

    # # get regional interest data
    # df = pytrends.interest_by_region(resolution="DMA")
    # # check if there is not enough data
    # if len(df[df.iloc[:, 0] == 100]) == 0:
    #     print("Not enough data for " + name)
    #     l_count += 1
    #     time.sleep(1)
    #     continue
    # # rename column[0] to movie_id
    # df = df.rename(columns={df.columns[0]: movie_id})
    # # append df to v2_df
    # v2_df = pd.concat([v2_df, df], axis=1)
    # df = pd.DataFrame()
    # df[movie_id] = [0]
    # df.loc[0, movie_id] = peak
    # # append df to v3_dfcd
    # v3_df = pd.concat([v3_df, df], axis=1)
    # print(name + " fourth request complete.")
    # # Delay for 1 second between requests
    # time.sleep(1)
    
    # save v1_df to csv
    v1_df.to_csv('movie_id_regional_data_all_time.csv', index=True)
    # # save v2_df to csv
    # v2_df.to_csv('movie_id_regional_data_around_peak.csv', index=True)
    # # save v3_df to csv
    # v3_df.to_csv('movie_id_peak_dates.csv', index=True)

### END OF LOOP ###

# print number and percent of data lost
l_percent = 100 * l_count / total
l_message = str(l_count) + " out of " + str(total) + " movies lost due to insufficient data. This reflects a loss of " + str(l_percent) + "%."
print(l_message)