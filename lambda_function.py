import json
import pandas as pd
import requests


def lambda_handler(event, context):

    print("Demo started...")
    print("Event data  -->", event)

    response = requests.get("https://www.google.com/")
    print(response.text)
    

    data={'col1': [1,2],'col2':[3,4]}
    df = pd.DataFrame(data)
    print(df)
    print("Demo completed !!")