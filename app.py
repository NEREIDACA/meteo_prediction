import dash
from dash import html, dcc, Output, Input
import plotly.express as px
import pandas as pd

app = dash.Dash(__name__)

catchment_points = {
    "Ter": [
        {"name": "Ripoll", "lat": 41.98, "lon": 2.53},
        {"name": "Girona", "lat": 41.98, "lon": 2.82}
    ],
    "Tordera": [
        {"name": "Palautordera", "lat": 41.68, "lon": 2.45},
        {"name": "Tordera", "lat": 41.71, "lon": 2.72}
    ]
}

points = []
for basin, sites in catchment_points.items():
    for site in sites:
        points.append({"basin": basin, "name": site["name"], "lat": site["lat"], "lon": site["lon"]})

df_map = pd.DataFrame(points)

fig = px.scatter_mapbox(
    df_map,
    lat="lat",
    lon="lon",
    hover_name="name",
    zoom=8,
    mapbox_style="open-street-map",
    custom_data=["basin"]  # ✅ Pass basin as customdata
)

app.layout = html.Div([
    dcc.Graph(id="map", figure=fig),
    html.Div(id="output")
])

@app.callback(
    Output("output", "children"),
    Input("map", "clickData")
)
def display_click_data(clickData):
    if clickData:
        point = clickData["points"][0]
        location_id = f"{point['customdata'][0]}_{point['hovertext']}"
        return html.Iframe(src=f"/static/{location_id}.html", width="100%", height="800px")
    return "Click on a location to view data."

if __name__ == "__main__":
    app.run(debug=True)

