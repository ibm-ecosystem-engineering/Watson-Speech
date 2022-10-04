import os
import math
import time
import dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash import dash_table, callback_context
import dash_daq as daq
from dash import Input, Output, State, html
from dash.dependencies import Input, Output
import datetime, random
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
import plotly.io as pio
import numpy as np
import re
import json
from dash.dependencies import Input, Output
from wordcloud import WordCloud
import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import watson_nlp
import io
import base64
import requests
import IPython.display as ipd
import librosa
import pandas as pd
import soundfile as sf

plt.switch_backend('Agg') 

external_stylesheets = ['assets/bootstrap.min.css']
app = dash.Dash(external_stylesheets=external_stylesheets)
app.title = 'Watson Text to Speech (TTS) Library'

# Setting theme for plotly charts
plotly_template = pio.templates["plotly_dark"]
pio.templates["plotly_dark_custom"] = pio.templates["plotly_dark"]

navbar_main = dbc.Navbar(
        [
            html.A(
                dbc.Row(
                    [
                    dbc.Col(html.Img(src=app.get_asset_url('ibm_logo.png'), height="30px")),
                    dbc.Col(dbc.NavbarBrand("Build Lab", className="ml-auto")),
                    #dbc.Col(html.H2("Watson NLP"), className="me-auto", justify='center')
                    ],
                    className="w-0",
                ),
                style={"textDecoration": "bold", "margin-right": "20%"},
            ),
            dbc.Col(
                [
                    dbc.Row(
                        [
                            html.H3("Watson Text to Speech (TTS) Library", style={'textAlign': 'center'}),
                            
                        ],
                        className="me-auto",
                        align='center',
                        justify='center',
                    ),
                ],
                align = 'center'
            ),
            dbc.Col([]),
        ],
    color="primary",
    dark=True,
    className = "ml-auto"
)

# Creating call method for TTS 
text_to_speech_url ='http://localhost:1080/text-to-speech/api/v1/synthesize'
# Setting up the headers for post request to service 
headers = {"Content-Type": "application/json","Accept":"audio/wav"}
params ={'voice':'en-US_AllisonV3Voice'}
file_name = "./TTS_Output/consumer_output.wav"
tts_sample_text = "I don't share everyone's unbridled enthusiasm for this film. It is indeed a great popcorn flick, with outstanding aerial photography and maneuvers. But 10 stars? There are few, if any, movies that are perfect, and deserve that kind of rating. \
The problem with the film is the plot. It is so filled with age-worn cliches that one could easily tell what was coming from beginning to end. I mean, you had to know who was going to save the day at the end, and you had to know what was going to happen when Maverick jumped out of Penny's window. Those are just two examples of the many obvious plot points that you could see coming a mile away. I could list them all, but it would take up too much space here. Basically the entire plot was entirely predictable. \
The opening scene, especially, was straight out of Hollywood Screenplay Writing 101. I mean, seriously, how many times have we seen that subplot? Countless. \
There were no characters in the movie, either. They were all caricatures, stereotypes. No depth to any of them. They had their standard roles to play, and that was it. \
Did I enjoy the film? Sure, it was fun. Especially on a big theater screen with a loud sound system. Did I take anything away from the film? Did it make me think about anything after it was over? Nah. Will I see it again? Nah. \
I will give Tom Cruise credit for including Val Kilmer in the cast. Considering his health problems, that was a nice touch. \
So, yeah, enjoy the film. Sit back with your bag of popcorn and enjoy the g-forces. But don't pretend it is anything other than just another summer blockbuster."

def seconds_to_MMSS(slider_seconds):
    decimal, minutes = math.modf(slider_seconds / 60.0)
    seconds = str(round(decimal * 60.0))
    if len(seconds) == 1:
        seconds = "0" + seconds
    MMSS = "{0}:{1}".format(round(minutes), seconds)
    return MMSS


tts_analysis_input =  dbc.InputGroup(
            [
                dbc.Textarea(id="tts-input", value=tts_sample_text,cols=150, placeholder="Text to Speech analysis"),
                dcc.Clipboard(
                    target_id="textarea-tts",
                    title="copy1",
                    style={
                        "display": "inline-block",
                        "fontSize": 20,
                        "verticalAlign": "top",
                        "color": "black"
                    },
                ),
                dbc.Button("Play", id="tts-button", className="me-2", n_clicks=0),
            ],
            className="mb-3",
        )

audio2 = html.Div(children=[
    html.Audio(html.Source(src="CallCenterSample1.mp3",type="audio/mp3"), controls=True)
])
app.layout = html.Div(children=[
                    navbar_main,
                dbc.Row(
                    [
                    dbc.Col(
                        children=[
                        html.Br(),
                        html.P(children="Use the sample text or enter your own text in English"),
                        html.Div(tts_analysis_input),
                        html.Br(),
                        html.Audio(id="player", src=file_name, controls=True, style={ "width": "100%"}),
                        html.Br(),
                        html.Br(),
                        html.Div(audio2),
                        #dcc.Graph(id="waveform", figure=plt.show()),
                        ],
                        # width=6
                    ),
                    ],
                    # align="center",
                    # className="w-0",
                ),
                html.Br(),
                html.Br(),
                html.Br(),
                html.Footer(children="Please note that this content is made available by IBM Build Lab to foster Embedded AI technology adoption. \
                                The content may include systems & methods pending patent with USPTO and protected under US Patent Laws. \
                                Copyright - 2022 IBM Corporation")
])

def print_plot_play(fileName, text=''):
    x, Fs = librosa.load(fileName, sr=None)
    print('%s Fs = %d, x.shape = %s, x.dtype = %s' % (text, Fs, x.shape, x.dtype))
    plt.figure(figsize=(10, 5))
    plt.plot(x, color='blue')
    plt.xlim([0, x.shape[0]])
    plt.xlabel('Time (samples)')
    plt.ylabel('Amplitude')
    plt.tight_layout()
    return plt


# method to get the Voice data from the text service 
def getSpeechFromText(headers,params,data,file_name):
    request =requests.post(text_to_speech_url,headers=headers,params =params,data=data)
    print(request.status_code)
    if request.status_code != 200:
        print("TTS Service status:", request.text)
    with open(file_name, mode='bx') as f:
        f.write(request.content)
    return file_name 



@app.callback(
    #Output("slider-output-container", "children"),
    #Output("waveform", "figure"),
    Output("player", "src"),
    Input('tts-button', 'n_clicks'),
    Input('tts-input', 'value')   
)

def update_output(n_clicks, value):
    print("Helooooo calling method---",value)
    text_data = '{"text":"I dont share everyones unbridled enthusiasm for this film. It is indeed a great popcorn flick, with outstanding aerial photography and maneuvers. But 10 stars?"}'
    file_name = './TTS_Output/result.wav'
    src =getSpeechFromText(headers,params,text_data,file_name)
    figure  =print_plot_play(file_name, "Hello")
    return src 
   

if __name__ == '__main__':
    SERVICE_PORT = os.getenv("SERVICE_PORT", default="8052")
    app.run(host="0.0.0.0", port=SERVICE_PORT, debug=True)
