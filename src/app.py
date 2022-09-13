import streamlit as st
import json
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go

# Add title and header
st.title("Renewable power plants in Switzerland")

st.write("Data 'renewable_power_plants_CH.csv' from:", "https://data.open-power-system-data.org/renewable_power_plants/")

# Widgets: checkbox (you can replace st.xx with st.sidebar.xx)
if st.checkbox("Show Dataframe"):
    st.subheader("This is my dataset:")
    st.dataframe(data=clean_energy_ch)
    # st.table(data=mpg_df)

st.header("Part 1")

clean_energy_ch = pd.read_csv("./data/renewable_power_plants_CH.csv")

# Getting the coordinates of the Cantons - file downloaded from here: https://data.opendatasoft.com/explore/dataset/georef-switzerland-kanton%40public/export/?disjunctive.kan_code&disjunctive.kan_name&sort=year&location=8,46.82242,8.22403&basemap=jawg.streets&dataChart=eyJxdWVyaWVzIjpbeyJjb25maWciOnsiZGF0YXNldCI6Imdlb3JlZi1zd2l0emVybGFuZC1rYW50b25AcHVibGljIiwib3B0aW9ucyI6eyJkaXNqdW5jdGl2ZS5rYW5fY29kZSI6dHJ1ZSwiZGlzanVuY3RpdmUua2FuX25hbWUiOnRydWUsInNvcnQiOiJ5ZWFyIn19LCJjaGFydHMiOlt7ImFsaWduTW9udGgiOnRydWUsInR5cGUiOiJsaW5lIiwiZnVuYyI6IkNPVU5UIiwic2NpZW50aWZpY0Rpc3BsYXkiOnRydWUsImNvbG9yIjoiIzE0MkU3QiJ9XSwieEF4aXMiOiJ5ZWFyIiwibWF4cG9pbnRzIjoiIiwidGltZXNjYWxlIjoieWVhciIsInNvcnQiOiIifV0sImRpc3BsYXlMZWdlbmQiOnRydWUsImFsaWduTW9udGgiOnRydWV9

with open("./data/georef-switzerland-kanton.geojson") as response:
    cantons = json.load(response)

#cantons["features"][0]["properties"]

# Need to find a way to match the canton code from the df with the canton name in the json

cantons_dict = {'TG':'Thurgau', 'GR':'Graubünden', 'LU':'Luzern', 'BE':'Bern', 'VS':'Valais',
                'BL':'Basel-Landschaft', 'SO':'Solothurn', 'VD':'Vaud', 'SH':'Schaffhausen', 'ZH':'Zürich',
                'AG':'Aargau', 'UR':'Uri', 'NE':'Neuchâtel', 'TI':'Ticino', 'SG':'St. Gallen', 'GE':'Genève',
                'GL':'Glarus', 'JU':'Jura', 'ZG':'Zug', 'OW':'Obwalden', 'FR':'Fribourg', 'SZ':'Schwyz',
                'AR':'Appenzell Ausserrhoden', 'AI':'Appenzell Innerrhoden', 'NW':'Nidwalden', 'BS':'Basel-Stadt'}

clean_energy_ch["canton_name"] = clean_energy_ch["canton"].map(cantons_dict)
#clean_energy_ch.info()

sources_per_canton = clean_energy_ch.groupby("canton_name").size().reset_index(name="count")
sources_per_canton.head()

fig = px.choropleth_mapbox(
    sources_per_canton,
    color="count",
    geojson=cantons,
    locations="canton_name",
    featureidkey="properties.kan_name",
    center={"lat": 46.8, "lon": 8.3},
    mapbox_style="open-street-map",
    zoom=6.3,
    opacity=0.8,
    width=900,
    height=500,
    labels={"canton_name":"Canton",
           "count":"Number of Sources"},
    title="<b>Number of Renewable Energy Sources per Canton</b>",
    color_continuous_scale="Cividis",
)
fig.update_layout(margin={"r":0,"t":35,"l":0,"b":0},
                  font={"family":"Sans",
                       "color":"maroon"},
                  hoverlabel={"bgcolor":"white",
                              "font_size":12,
                             "font_family":"Sans"},
                  title={"font_size":20,
                        "xanchor":"left", "x":0.01,
                        "yanchor":"bottom", "y":0.95}
                 )
#fig.show()
st.plotly_chart(fig)


