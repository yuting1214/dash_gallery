import dash
from dash import dcc, html, Input, Output, State, ALL
from dash.exceptions import PreventUpdate 

# Sample stock data
stock_data = ['1234', '1101', '1111','5678', '9876', '5432', '8765', '4321', '2468', '1357', '9753', '8642']

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the layout of the app
app.layout = html.Div([
    dcc.Input(id='search-input', type='text', placeholder='Enter a stock ID...'),
    html.Div(id='search-output')
])

# Define callback to update the output based on the search input
@app.callback(
    [Output('search-output', 'children', allow_duplicate=True),
     Output('search-input', 'value', allow_duplicate=True)],
    [Input('search-input', 'value')],
    prevent_initial_call=True
)
def update_output(search_term):
    if not search_term:
        return html.P('Enter a stock ID to search.'), ''
    
    filtered_data = [stock_id for stock_id in stock_data if stock_id.startswith(search_term)]
    
    if not filtered_data:
        return html.P('No matching stock IDs found.'), search_term
    
    if len(filtered_data) == 1 and filtered_data[0] == search_term:
        return (
            html.P(f'You clicked on: {filtered_data[0]}'),
            filtered_data[0]
        )
    
    return (
        html.Ul(
            children=[
                html.Li(
                    html.Button(stock_id, id={'type': 'stock-id', 'index': i}),
                    style={'display': 'inline-block', 'marginRight': '10px'}  # Adjust spacing between buttons
                )
                for i, stock_id in enumerate(filtered_data)
            ]
        ),
        search_term)

# Define callback to handle clicks on stock IDs
@app.callback(
    Output('search-input', 'value'),
    [Input({'type': 'stock-id', 'index': ALL}, 'n_clicks')],
    [State('search-output', 'children')],
    prevent_initial_call=True
)
def handle_clicks(n_clicks, children):
    if n_clicks is None or all((x == 0) or (x is None) for x in n_clicks):
        raise PreventUpdate
    else:
        clicked_index = [index for index, n_clicks in enumerate(n_clicks) if n_clicks is not None][0]
        clicked_stock_id = children['props']['children'][clicked_index]['props']['children']['props']['children']
        return clicked_stock_id

if __name__ == '__main__':
    # Run the app
    app.run_server(debug=True)
