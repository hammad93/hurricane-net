config = {
    'api_url' : 'http://fluids.ai:1337/'
}
import requests
import pandas as pd
import openai
import json
import os

def chatgpt_forecast_live():
    '''
    This will pull in the live storms across the globe and engineer
    prompts that will allow us to ingest forecasts from ChatGPT

    Returns
    -------
    list(pd.DataFrame) A list of DataFrames that have the columns
        id, time, lat, lon, and wind_speed
    '''
    # get the current live tropical storms around the globe
    live_storms = get_live_storms()
    prompts = get_prompts(live_storms)
    # capture the forecast from ChatGPT
    forecasts = []
    for prompt in prompts:
        forecasts.append(chatgpt_forecast(prompt))
    return forecasts

def chatgpt_forecast(prompt):
    '''
    Given the prompt, this will pass it to the version of ChatGPT defined.
    It's meant for forecasts of global tropical storms but can have a range of options.

    Input
    -----
    prompt String
        The initial message to pass to ChatGPT
    system String
        The system message based on the current OpenAI API
    
    Returns
    -------
    pd.DataFrame
    '''
    openai.api_key = os.environ.get('OPENAI_API_KEY')
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
                {"role": "system", "content": "Please act as a forecaster and a helpful assistant. Responses should be based on historical data and forecasts must be as accurate as possible."},
                {"role": "user", "content": prompt},
            ]
        )
    text = response["choices"][0]["message"]["content"]
    print(text)
    # Find the indices of the first and last curly braces in the text
    start_index = text.find('{')
    end_index = text.rfind('}')

    # Extract the JSON string from the text
    json_string = text[start_index:end_index+1]

    # Parse the JSON string into a Python object
    json_object = json.loads(json_string)

    # Extract the relevant information from the object
    forecasts = json_object['forecasts']

    return pd.DataFrame(forecasts)

def get_live_storms():
    '''
    Upon calling this function, the live tropical storms around the global
    will be returned in a JSON format. Each of the storms returned will have
    the historical records along with in.

    Returns
    -------
    df pandas.DataFrame
        The records include the columns id, time, lat, lon, wind_speed
    '''
    # make the request for live data
    response = requests.get(f"{config['api_url']}live-storms")
    if response :
        data = response.json()
    else :
        print(f'There was an error getting live storms, {response.content}')
        return response
    return pd.DataFrame(data)

def get_prompts(df):
    '''
    Utilizing the current global tropical storms, we will generate prompts
    for a LLM such as ChatGPT to provide forecasts. This function will
    generate prompts for each storm

    Intput
    ------
    df pd.DataFrame
        The records include the columns id, time, lat, lon, wind_speed.
    '''
    unique_storms = set(df['id'])
    prompts = []
    # apply each storm to the prompt template
    for storm in unique_storms:
        prompt = f'''
I want you to act like a forecaster that gives a general idea of the future of the storm even though it will not be an official forecast.
Please provide forecasts for 12, 24, 36, 48, 72, 96, 120 hours in the future from the most recent time in Figure 1.
The response will be JSON formatted with "forecasts" as the only key. The value of the key is a list of forecast objects.
Each forecast object has five attributes:
    "id" which identifies the storm
    "time" which is the predicted time in ISO 8601 format
    "lat" which is the predicted latitude in decimal degrees
    "lon" which is the predicted longitude in decimal degrees
    "wind_speed" which is the predicted maximum sustained wind speed in knots.
The response must be in JSON format, and the JSON characters must be at the beginning of the response.
If you wish to add additional comments, it must be after the JSON data.

Figure 1. The historical records the includes columns representing measurements for storm {storm}.
The wind_speed column is in knots representing the maxiumum sustained wind speeds.
The lat and lon are the geographic coordinates in decimal degrees.

In JSON,
{df[df['id'] == storm].to_json()}
        '''
        prompts.append(prompt)
        print(prompt)
    return prompts
