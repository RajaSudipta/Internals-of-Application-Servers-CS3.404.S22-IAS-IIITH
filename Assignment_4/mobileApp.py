from urllib import response
import requests
import pickle
import base64

# data processing
import pandas as pd 

# Saving Model
import pickle

url = "http://localhost:8000/getResult"

''' Read the eval data from eval.csv, keep it in a dataframe '''
test_df = pd.read_csv("eval.csv")

''' wrapping the dataframe into a string to send to server '''
pickled = pickle.dumps(test_df)
pickled_b64 = base64.b64encode(pickled)
hug_pickled_str = pickled_b64.decode('utf-8')
# print(hug_pickled_str)

''' sending the data to server '''
response = requests.post(url, data=hug_pickled_str)

''' Printing Passenger ID's '''
passengerId_df = test_df["PassengerId"]
# print(passengerId_df)
passengerId_list = passengerId_df.tolist()
print("Passenger List: ")
print(passengerId_list)

''' Printing model calculated result '''
print("Model calculated survival result of passengers: ")
print(response.content.decode())

''' Finding out the expected result from gender_submission.csv '''
# excepted_res_df = pd.read_csv("gender_submission.csv")
# excepted_res_df_valid_passengers = excepted_res_df[excepted_res_df['PassengerId'].isin(passengerId_list)]
# expected_survival_list = excepted_res_df_valid_passengers['Survived'].to_list()
# print("Expected survival result of passengers: ")
# print(expected_survival_list)
