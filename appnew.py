import pickle
import pandas as pd
import webbrowser
import dash
import dash_html_components as html
import dash_core_components as dcc
import plotly.express as px
from dash.dependencies import Input, Output ,State
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer


# Declaring Global variables
app = dash.Dash()
project_name = None

def load_model():
    global df
    df = pd.read_csv('balanced_reviews.csv')
  
    global pickle_model
    file = open("pickle_model.pkl", 'rb') 
    pickle_model = pickle.load(file)

    global vocab
    file = open("feature.pkl", 'rb') 
    vocab = pickle.load(file)
    
    print(df.sample(5))

def open_browser():
    #default web browser
    webbrowser.open_new('http://127.0.0.1:8050/')

def check_review(reviewText):

    #reviewText has to be vectorised, that vectorizer is not saved yet
    #load the vectorize and call transform and then pass that to model preidctor
    #load it later

    transformer = TfidfTransformer()
    loaded_vec = CountVectorizer(decode_error="replace",vocabulary=vocab)
    reviewText = transformer.fit_transform(loaded_vec.fit_transform([reviewText]))
    return pickle_model.predict(reviewText)
 
def create_app_ui():
    
    global df2
    df2= pd.read_csv('newreview.csv')
    
    
    # Create the UI of the Webpage
    main_layout = html.Div(
    [
    html.H1(children='Sentiments Analysis with Insights', id='Main_title',
            style={'textAlign': 'center','color':'Black'}),
    
    #review
    html.H1(children='Review', id='Main_titlesub2',
            style={'textAlign': 'left','color':'Blue'}),
    
    #piechart 
    html.H1(children='Pie Chart', id='Main_titlesub1',
            style={'textAlign': 'center','color':'Red'}),
    dcc.Graph(id='piechart'),
    html.H1(id="chart"),#{'label':'Positive','value':1},{'label':'negative','value':0}),
   
    #drop
    dcc.Dropdown(
        id='drop_down',
        options = [
            {'label': i,'value': i} for i in df2['reviews_df'].sample(50)
            ],
        ),
    
    html.Button(children='Find Review', id='button_click', n_clicks=0,
                style={'color':'Black'}),
    
    html.H1(children=None, id='result', style={'textAlign': 'left','color':'Black'}),
    
    
    dcc.Textarea(
        id='textarea_review',
        placeholder='Enter reviews',
        style={'width': '80%', 'height': 80, 'background':'Green'},
        ),
    
    html.Button(children='Find Review', id='button_click1', n_clicks=0,),
    
    html.H1(children=None, id='result1', style={'textAlign': 'center','color':'Black'}),
    ]
    )
    return main_layout
    

@app.callback(
    Output("piechart", "figure"), 
    [Input("chart", "value")
     ])
def generate_chart(chart):
    df1=px.data.tips()
    
    diagram = px.pie(
        data_frame=df1,
        names=chart)
    return diagram


@app.callback(
    Output('result1', 'children'),
    [
    Input('button_click1', 'n_clicks')
    ],
    [
    State('textarea_review', 'value') 
    ]
    )
def update_app_ui(n_clicks,textarea_value):
    
    print("Data Type= ", str(type(textarea_value)))
    print("Value= ", str(textarea_value))

    
    result_list = check_review(textarea_value)
    
    if (result_list[0] == 0 ):
        result = 'Negative'
    elif (result_list[0] == 1 ):
        result = 'Positive'
    else:
        result = 'default'
    return result


@app.callback(
    Output('result', 'children'),
    [
    Input('button_click', 'n_clicks'), 
    ],
    [
    State('drop_down','value') ,
    ]
    )
def update_app_ui_drop(n_clicks,drop_down):
    
    print("Data Type= ", str(type(drop_down)))
    print("Value= ", str(drop_down))

    
    result_list = check_review(drop_down)
    if (result_list[0] == 0 ):
        result = 'Negative'
    elif (result_list[0] == 1 ):
        result = 'Positive'
    else:
        result = 'default'    
    return result
    
    
# Main Function to control the Flow of your Project
def main():
    load_model()    
    open_browser()
    
    global project_name
    project_name = "Sentiments Analysis with Insights" 
      
    global app
    app.layout = create_app_ui()
    app.title = project_name
    app.run_server()
  
    print("This would be executed when the script is closed")
    app = None
    project_name = None

if __name__ == '__main__':
    main()
