from flask import Flask
from dash import Dash, dcc, html, Input, Output
import pandas as pd
import plotly.express as px

# Create a Flask server instance.
server = Flask(__name__)

# Create a Dash app and pass the Flask server.
app = Dash(__name__, server=server)

# ---------------------------
# Load DataFrames
# ---------------------------
dataset_paths = {
    'Rental Index': 'df_rental_index_avg.csv',
    'Value Index': 'df_value_index_avg.csv',
    'Market Index': 'df_market_index_avg.csv',
    'New Construction Count': 'df_newcon_count_avg.csv',
    'New Construction Sales': 'df_newcon_sales_avg.csv',
    'Days Pending': 'df_days_pending_avg.csv',
}

def load_dataset(path):
    df = pd.read_csv(path)
    df = df.drop(columns=['_id', 'RegionID', 'SizeRank', 'RegionType'], errors='ignore')
    return df

dataframes = {name: load_dataset(path) for name, path in dataset_paths.items()}

# ---------------------------
# App Layout
# ---------------------------
app.layout = html.Div([
    html.H1("US Real Estate Dashboard"),
    
    html.Div([
         html.Label("Select Dataset:"),
         dcc.Dropdown(
             id="dataset-dropdown",
             options=[{"label": k, "value": k} for k in dataframes.keys()],
             value="Value Index",
             placeholder="Select Dataset"
         )
    ], style={'width': '30%', 'display': 'inline-block'}),
    
    html.Br(),

    html.Div([
         html.Label("Select Year:"),
         dcc.RadioItems(
             id="year-radio",
             labelStyle={'display': 'inline-block', 'margin-right': '15px'}
         )
    ], style={'width': '80%', 'padding': '20px'}),
    
    html.Br(),

    html.Div([
         dcc.Graph(id="map-graph")
    ]),

    # New controls for sorting and number of cities
    html.Div([
        html.Label("Sort Order:"),
        dcc.RadioItems(
            id="sort-order",
            options=[
                {"label": "Cities with Highest Average", "value": "desc"},
                {"label": "Cities with Lowest Average", "value": "asc"},
            ],
            value="desc",
            labelStyle={'display': 'inline-block', 'margin-right': '15px'}
        ),
        html.Label("Number of Cities:"),
        dcc.Dropdown(
            id="city-count",
            options=[{"label": str(i), "value": i} for i in [10, 20, 50, 100]],
            value=10,
            style={"width": "150px", "display": "inline-block", "margin-left": "10px"}
        )
    ], style={'padding': '20px'}),

    html.Div([
         dcc.Graph(id="bar-graph")
    ]),

    html.Br(),

    html.Div([
         html.Label("Select City for Trend:"),
         dcc.Dropdown(
             id="city-dropdown",
             placeholder="Select City"
         )
    ], style={'width': '30%', 'display': 'inline-block'}),
    
    html.Br(),
    
    html.Div([
         dcc.Graph(id="line-graph")
    ])
])

# ---------------------------
# Callback: Update Year Radio Options
# ---------------------------
@app.callback(
    [Output('year-radio', 'options'),
     Output('year-radio', 'value')],
    Input('dataset-dropdown', 'value')
)
def update_year_radio(dataset_name):
    df = dataframes[dataset_name]
    years = []
    for col in df.columns:
        if col.startswith(f"{dataset_name} "):
            year_part = col.split(f"{dataset_name} ")[1]
            try:
                y = int(year_part)
                years.append(y)
            except:
                pass
    if not years:
        years = [int(col) for col in df.columns if col.isdigit()]
    years = sorted(list(set(years)))
    if not years:
        years = [2000]
    options = [{"label": str(year), "value": year} for year in years]
    default = max(years)
    return options, default

# ---------------------------
# Callback: Update City Dropdown
# ---------------------------
@app.callback(
    [Output('city-dropdown', 'options'),
     Output('city-dropdown', 'value')],
    Input('dataset-dropdown', 'value')
)
def update_city_dropdown(dataset_name):
    df = dataframes[dataset_name]
    city_col = "RegionName" if "RegionName" in df.columns else "City"
    cities = sorted(df[city_col].dropna().unique())
    options = [{"label": city, "value": city} for city in cities]
    default = "New York City" if "New York City" in cities else (cities[0] if cities else None)
    return options, default

# ---------------------------
# Callback: Map Graph
# ---------------------------
@app.callback(
    Output("map-graph", "figure"),
    [Input("dataset-dropdown", "value"), Input("year-radio", "value")]
)
def update_map(selected_dataset, selected_year):
    selected_year_str = str(selected_year)
    df = dataframes[selected_dataset].copy()
    df.columns = df.columns.str.strip()
    
    preferred_col = f"{selected_dataset} {selected_year_str}"
    col_name = preferred_col if preferred_col in df.columns else selected_year_str
    
    lat_col = "latitude" if "latitude" in df.columns else "Latitude"
    lon_col = "longitude" if "longitude" in df.columns else "Longitude"
    
    df_map = df.dropna(subset=[col_name, lat_col, lon_col])
    
    fig = px.scatter_mapbox(
        df_map,
        lat=lat_col,
        lon=lon_col,
        size=col_name,
        color=col_name,
        hover_name="RegionName",
        hover_data={
            "StateName": False,
            col_name: True,
            lat_col: False,
            lon_col: False
        },
        labels = {col_name: f"{col_name} Average {selected_dataset}"},
        zoom=3,
        height=600,
        color_continuous_scale="Viridis"
    )
    
    fig.update_layout(
        mapbox_style="carto-positron",
        mapbox_center={"lat": 37.0902, "lon": -95.7129},
        mapbox_zoom=4,
        margin={"r": 0, "t": 0, "l": 0, "b": 0}
    )
    
    return fig

# ---------------------------
# Callback: Bar Graph
# ---------------------------
@app.callback(
    Output("bar-graph", "figure"),
    [
        Input("dataset-dropdown", "value"),
        Input("year-radio", "value"),
        Input("sort-order", "value"),
        Input("city-count", "value")
    ]
)
def update_bar_chart(selected_dataset, year, sort_order, city_count):
    selected_year = str(year)
    df = dataframes[selected_dataset]
    col = selected_year if selected_year in df.columns else f"{selected_dataset} {selected_year}"
    region_col = "RegionName" if "RegionName" in df.columns else "City"

    df_filtered = df[df[region_col] != 'United States'][[region_col, col]].dropna()
    ascending = True if sort_order == "asc" else False
    df_filtered = df_filtered.sort_values(by=col, ascending=ascending).head(city_count)

    us_row = df[df[region_col] == 'United States']
    us_val = us_row[col].values[0] if not us_row.empty else None

    fig = px.bar(df_filtered, x=region_col, y=col,
                 title=f"Top {city_count} Cities ({'Ascending' if ascending else 'Descending'}) - {selected_year}",
                 color_discrete_sequence=['#5DADE2'])

    if us_val is not None:
        fig.add_hline(y=us_val, line_dash="dot", line_color="red", annotation_text="US Average")

    fig.update_layout(xaxis_tickangle=45, height=600)
    return fig

# ---------------------------
# Callback: Line Graph
# ---------------------------
@app.callback(
    Output("line-graph", "figure"),
    [Input("dataset-dropdown", "value"), Input("city-dropdown", "value")]
)
def update_line_graph(selected_dataset, selected_city):
    df = dataframes[selected_dataset]
    city_col = "RegionName" if "RegionName" in df.columns else "City"
    if selected_city is None or selected_city not in df[city_col].unique():
        return {}
    city_df = df[df[city_col] == selected_city]
    if city_df.empty:
        return {}

    exclude = {city_col, "Latitude", "Longitude", "State", "StateName", "RegionName"}
    trend_data = {}
    for col in city_df.columns:
        if col in exclude:
            continue
        if col.startswith(f"{selected_dataset} "):
            year_part = col.split(f"{selected_dataset} ")[1]
        else:
            year_part = col
        try:
            year_int = int(year_part)
            trend_data[year_int] = city_df[col].values[0]
        except:
            continue
    if not trend_data:
        return {}
    trend_df = pd.DataFrame(list(trend_data.items()), columns=["Year", "Value"])
    trend_df = trend_df.sort_values(by="Year")
    title = f"{selected_dataset} Trend for {selected_city}"
    fig = px.line(trend_df, x="Year", y="Value", title=title)
    fig.update_layout(xaxis_title="Year", yaxis_title=selected_dataset)
    return fig

# ---------------------------
# Run the App
# ---------------------------
if __name__ == '__main__':
    app.run(debug=True, port=8058)