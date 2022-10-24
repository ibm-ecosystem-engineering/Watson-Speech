import os
import dash
from dash import dcc
import dash_bootstrap_components as dbc
from dash import Input, Output, html, State
import plotly.io as pio
from dash.dependencies import Input, Output
import matplotlib.pyplot as plt
import requests
import librosa


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
                    #dbc.Col(html.Img(src=app.get_asset_url('ibm_logo.png'), height="40px")),
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

# Creating call method for TTS 
text_to_speech_url = os.getenv("TTS_SERVICE_URL", default='http://0271714b-us-south.lb.appdomain.cloud:1080/text-to-speech/api/v1/synthesize')
# Setting up the headers for post request to service 
headers = {"Content-Type": "application/json","Accept":"audio/wav"}
params ={'voice':'en-US_AllisonV3Voice'}
file_name = "assets/result.wav"
tts_sample_text = "I don't share everyone's unbridled enthusiasm for this film. It is indeed a great popcorn flick, with outstanding aerial photography and maneuvers. But 10 stars? There are few, if any, movies that are perfect, and deserve that kind of rating. \
The problem with the film is the plot. It is so filled with age-worn cliches that one could easily tell what was coming from beginning to end. I mean, you had to know who was going to save the day at the end, and you had to know what was going to happen when Maverick jumped out of Penny's window. Those are just two examples of the many obvious plot points that you could see coming a mile away. I could list them all, but it would take up too much space here. Basically the entire plot was entirely predictable. \
The opening scene, especially, was straight out of Hollywood Screenplay Writing 101. I mean, seriously, how many times have we seen that subplot? Countless. \
There were no characters in the movie, either. They were all caricatures, stereotypes. No depth to any of them. They had their standard roles to play, and that was it. \
Did I enjoy the film? Sure, it was fun. Especially on a big theater screen with a loud sound system. Did I take anything away from the film? Did it make me think about anything after it was over? Nah. Will I see it again? Nah. \
I will give Tom Cruise credit for including Val Kilmer in the cast. Considering his health problems, that was a nice touch. \
So, yeah, enjoy the film. Sit back with your bag of popcorn and enjoy the g-forces. But don't pretend it is anything other than just another summer blockbuster."

tts_analysis_input =  dbc.InputGroup(
            [
                # dbc.Textarea(id="tts-input", value=tts_sample_text,cols=150,rows=8,persistence=True,persistence_type='session', placeholder="Text to Speech analysis"),
                dbc.Textarea(id="tts-input", value=tts_sample_text,cols=150,rows=8, placeholder="Text to Speech analysis"),
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

audio2 = html.Div(children=[
    html.Audio(html.Source(src=file_name,type="audio/wav"), controls=True,style={ "width": "100%"})
])

image_path='assets/output.png'

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
                            # dcc.Dropdown(["Allison","Michael"], "Allison", id='voice_dropdown',persistence=True,persistence_type='session',style={'color':'#00361c'})
                            dcc.Dropdown(["Allison","Michael"], "Allison", id='voice_dropdown',style={'color':'#00361c'})
                        ),
                        dbc.Col(width=2),
                        ]
                        ),
                        html.Div(tts_analysis_input),
                        html.Br(),
                        # html.Div(audio2),
                        html.Div(id="div-audio", children=[' ']),
                        html.P(children="Text To Speech Output wave form"),
                        html.Img(src=image_path,style={ "width": "99%","height":"28%",'textAlign': 'center','margin-right':'100px'}),
                        ]
                    ),
                    ],
                ),
                html.Br(),
                html.Label("This App was built using Watson NLP library."),
                html.Br(),
                html.Footer(children="Please note that this content is made available by IBM Build Lab to foster Embedded AI technology adoption. \
                                The content may include systems & methods pending patent with USPTO and protected under US Patent Laws. \
                                Copyright - 2022 IBM Corporation")
])




# method to get the Voice data from the text service 
def getSpeechFromText(headers,params,data,file_name,voice_dropdown):
    if voice_dropdown =='Michael':
        params ={'voice':'en-US_MichaelV3Voice'}
    request =requests.post(text_to_speech_url,headers=headers,params =params,data=data)
    print(request.status_code)
    if request.status_code != 200:
        print("TTS Service status:", request.text)
    if os.path.exists(file_name):
        os.remove(file_name)
    with open(file_name, mode='bx') as f:
        f.write(request.content)



@app.callback(
    Output('div-audio', 'children'),
    Input('tts-button', 'n_clicks'),
    State('tts-input', 'value'),
    Input('voice_dropdown', 'value') 
)
def update_output(n_clicks, value,voice_dropdown):
    # if  n_clicks > 0:
    print("INPUT TEXT:", value)
    print(voice_dropdown)
    text_data = '{"text":"'+value+'"}'
    file_name = 'assets/result.wav'
    image_path ='assets/output.png'
    getSpeechFromText(headers,params,text_data,file_name,voice_dropdown)
    plt =print_plot_play(file_name, "Text To Speech Wav form")
    plt.savefig(image_path)
    return audio2,image_path


if __name__ == '__main__':
    SERVICE_PORT = os.getenv("SERVICE_PORT", default="8052")
    app.run(host="0.0.0.0", port=SERVICE_PORT, debug=True, dev_tools_hot_reload=False)
