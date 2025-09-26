# dashboard_cool.py
import dash
from dash import html, dcc
import pandas as pd
from dash.dependencies import Output, Input
from datetime import datetime

CSV_FILE = "attendance.csv"

app = dash.Dash(__name__)
server = app.server

# Layout with card-like design
app.layout = html.Div([
    html.H1("🎓 Attendance Dashboard", style={'textAlign': 'center', 'color': '#2c3e50'}),
    dcc.Interval(id='interval-component', interval=5000, n_intervals=0),  # refresh every 5 sec
    
    html.Div([
        html.Div([
            html.H3("📋 All Attendance Records", style={'color': '#34495e'}),
            html.Div(id='all-attendance', style={'maxHeight': '300px', 'overflowY': 'auto', 
                                                 'border': '1px solid #ccc', 'padding': '10px',
                                                 'borderRadius': '10px', 'backgroundColor': '#ecf0f1'})
        ], style={'width': '48%', 'display': 'inline-block', 'verticalAlign': 'top', 'marginRight': '2%'}),
        
        html.Div([
            html.H3("✅ Attendance Today", style={'color': '#27ae60'}),
            html.Div(id='today-attendance', style={'maxHeight': '300px', 'overflowY': 'auto',
                                                   'border': '1px solid #ccc', 'padding': '10px',
                                                   'borderRadius': '10px', 'backgroundColor': '#ecf0f1'})
        ], style={'width': '48%', 'display': 'inline-block', 'verticalAlign': 'top'}),
    ], style={'marginBottom': '20px'}),
    
    html.H3("📊 Attendance Summary", style={'color': '#2980b9'}),
    dcc.Graph(id='summary-graph', style={'border': '1px solid #ccc', 'borderRadius': '10px', 'padding': '10px'})
], style={'fontFamily': 'Arial, sans-serif', 'margin': '20px'})

@app.callback(
    [Output('all-attendance', 'children'),
     Output('today-attendance', 'children'),
     Output('summary-graph', 'figure')],
    [Input('interval-component', 'n_intervals')]
)
def update_dashboard(n):
    try:
        df = pd.read_csv(CSV_FILE)
    except FileNotFoundError:
        return "No records", "No records", {}

    # All attendance table
    all_table = html.Table([
        html.Tr([html.Th(col, style={'padding': '5px', 'borderBottom': '1px solid #7f8c8d'}) for col in df.columns])] +
        [html.Tr([html.Td(df.iloc[i][col], style={'padding': '5px'}) for col in df.columns]) for i in range(len(df))]
    )

    # Today’s attendance
    today = str(datetime.now().date())
    df_today = df[df["date"] == today]
    today_table = html.Table([
        html.Tr([html.Th(col, style={'padding': '5px', 'borderBottom': '1px solid #7f8c8d'}) for col in df_today.columns])] +
        [html.Tr([html.Td(df_today.iloc[i][col], style={'padding': '5px', 'color': '#27ae60', 'fontWeight': 'bold'}) for col in df_today.columns]) for i in range(len(df_today))]
    )

    # Summary graph
    summary = df.groupby("name").size().reset_index(name="Days Present")
    fig = {
        'data': [{'x': summary['name'], 'y': summary['Days Present'], 'type': 'bar', 'marker': {'color': '#2980b9'}}],
        'layout': {'title': 'Total Days Present', 'plot_bgcolor': '#ecf0f1', 'paper_bgcolor': '#ecf0f1',
                   'xaxis': {'title': 'Name'}, 'yaxis': {'title': 'Days Present'}}
    }

    return all_table, today_table, fig

if __name__ == '__main__':
    app.run(debug=True)