import os
import dash
from dash import dcc
import dash_bootstrap_components as dbc
from dash import Input, Output, html, State
import plotly.io as pio
from dash.dependencies import Input, Output
import matplotlib.pyplot as plt
import plotly.express as px
import requests
import librosa
import base64

plt.switch_backend('Agg') 

external_stylesheets = ['assets/bootstrap.min.css']
app = dash.Dash(external_stylesheets=external_stylesheets)
app.title = 'Watson Text to Speech (TTS) Library'


# Setting theme for plotly charts
plotly_template = pio.templates["plotly_dark"]
pio.templates["plotly_dark_custom"] = pio.templates["plotly_dark"]
app = dash.Dash(__name__, assets_folder=os.path.join(os.path.dirname(__file__), 'assets'))


navbar_main = dbc.Navbar(
        [
            html.A(
                dbc.Row(
                    [
                    dbc.Col([]),
                    dbc.Col([]),
                    dbc.Col([]),
                    dbc.Col(dbc.NavbarBrand("IBM Build Lab", className="ml-auto"), align='center'),
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
                            html.H2("Watson Text to Speech", style={'textAlign': 'center'}),
                            
                        ],
                        className="me-auto",
                        align='center',
                        justify='center',
                    ),
                ],
                align = 'center'
            ),
            dbc.Col(
                [
                    dbc.Row(
                        [   dbc.Col([]),
                            dbc.Col([]),
                            #dbc.Col(html.Img(src=app.get_asset_url('ibm_logo.png'), height="60px"))
                        ],
                        className='me-auto',
                        align='center',
                        justify='right',
                    ),  
                ],
                align = 'center'
            ),
        ],
    color="#003a6d",
    dark=True,
    className = "ml-auto"
)

wave_figure = dcc.Graph(id='wave-figure')

# Creating call method for TTS 
text_to_speech_url = os.getenv("TTS_SERVICE_URL", default='http://0271714b-us-south.lb.appdomain.cloud:1080/text-to-speech/api/v1/synthesize')
# Setting up the headers for post request to service 
headers = {"Content-Type": "application/json","Accept":"audio/wav"}
params ={'voice':'en-US_AllisonV3Voice'}
file_name = "assets/result.wav"
tts_sample_text = "Welcome to Watson Text to speech service demo. Watson Text to Speech service supports a wide variety of voices in all supported languages and dialects."

tts_analysis_input =  dbc.InputGroup(
            [
                dbc.Textarea(id="tts-input", value=tts_sample_text,cols=150,rows=5,persistence=True,persistence_type='session', placeholder="Text to Speech analysis"),
                # dbc.Textarea(id="tts-input", value=tts_sample_text,cols=150,rows=8, placeholder="Text to Speech analysis"),
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
                dbc.Button("Play", id="tts-button", className="me-2",n_clicks=0),
            ],
            className="mb-3",
        )

'''
audio2 = html.Div(children=[
    html.Audio(html.Source(src=file_name,type="audio/wav"), controls=True,preload='auto',style={ "width": "100%"})
])
'''


#image_path='assets/output.png'

def print_plot_play(fileName, text=''):
    x, Fs = librosa.load(fileName, sr=None)
    print('%s Fs = %d, x.shape = %s, x.dtype = %s' % (text, Fs, x.shape, x.dtype))
    fig = px.line(y=x)
    fig.update_layout(xaxis_title="Time (samples)", yaxis_title="Amplitude", title="Text To Speech Output wave form")
    '''
    plt.figure(figsize=(10, 5))
    plt.plot(x, color='blue')
    plt.xlim([0, x.shape[0]])
    plt.xlabel('Time (samples)')
    plt.ylabel('Amplitude')
    plt.tight_layout()
    '''

    return fig

app.layout = html.Div(children=[
                    navbar_main,
                dbc.Row(
                    [
                    dbc.Col(
                        children=[
                        html.Br(),
                        dbc.Row(
                        [
                            dbc.Col(html.P(children="Use the sample text or enter your own text in English"),width=8, lg=3),
                            dbc.Col(width=3),
                            dbc.Col(html.P(children="Select option for Enhanced neural voice")),
                            dbc.Col(
                                dcc.Dropdown(["Allison","Michael"], "Allison", id='voice_dropdown',persistence=True,persistence_type='session',style={'color':'#00361c'})
                            ),
                            dbc.Col(width=2),
                        ]
                        ),
                        html.Div(tts_analysis_input),
                        html.Br(),
                        html.Div(id="div-audio", children=[' ']),
                        html.Br(),
                        #html.Audio(html.Source(src=file_name1,type="audio/wav"),id="audio1", controls=True,preload='auto',style={ "width": "100%"})
                        #html.P(children="Text To Speech Output wave form"),
                        html.Div(wave_figure),
                        #html.Img(src=image_path,style={ "width": "99%","height":"28%",'textAlign': 'center','margin-right':'100px'}),
                        ]
                    ),
                    ],
                ),
                html.Br(),
                html.Label("This App was built using Watson Speech library.",style={"bottom":"25px","position": "absolute"}),
                #html.Br(),
                html.Footer(children="Please note that this content is made available by IBM Build Lab to foster Embedded AI technology adoption. \
                                The content may include systems & methods pending patent with USPTO and protected under US Patent Laws. \
                                Copyright - 2022 IBM Corporation",style={"bottom":"0px","position": "absolute"})
])

# method to get the Voice data from the text service 
def getSpeechFromText(headers,params,data,voice_dropdown):
    if voice_dropdown =='Michael':
        params ={'voice':'en-US_MichaelV3Voice'}
    request =requests.post(text_to_speech_url,headers=headers,params =params,data=data)
    print(request.status_code)
    file_data = file_name
    if request.status_code != 200:
        print("TTS Service status:", request.text)
    if os.path.exists(file_name):
        os.remove(file_name)
    with open(file_data, mode='bx') as f:
        f.write(request.content)
    return file_data
        

@app.callback(
    Output('div-audio', 'children'),
    Output('wave-figure', 'figure'),
    Input('tts-button', 'n_clicks'),
    State('voice_dropdown', 'value'),
    State('tts-input', 'value')
)

def update_output(n_clicks, voice_dropdown, text_input):
        print("INPUT TEXT:", text_input)
        print(voice_dropdown)
        text_data = '{"text":"' + text_input + '"}'
        file_data=getSpeechFromText(headers,params,text_data,voice_dropdown)
        plt = print_plot_play(file_name, "Text To Speech Wav form")
        #plt.savefig(image_path)
        print("file_data---",file_data)
        data_sound = base64.b64encode(open(file_data, 'rb').read())
        audio3 = html.Audio(id='audiospeler',
               src='data:audio/wav;base64,{}'.format(data_sound.decode()),
               controls=True,
               autoPlay=False,
               style={"width": "100%"}
               )
        return audio3 , plt


if __name__ == '__main__':
    SERVICE_PORT = os.getenv("SERVICE_PORT", default="8052")
    app.run(host="0.0.0.0", port=SERVICE_PORT, debug=True, dev_tools_hot_reload=False)
