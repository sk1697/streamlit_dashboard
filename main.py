import streamlit as st
import pandas as pd
import numpy as np
import geopandas as gpd
import folium
from streamlit_folium import st_folium
import os

print("구동되는중...")
st.set_page_config(page_title='test dashboard',page_icon='./static/icon.ico',layout='wide')

# 정적 파일 폴더 경로 설정
static_folder_path = os.path.join(os.getcwd(), "static")

# 사용자 정의 아이콘 이미지 경로
icon_image_path = 'http://localhost:8501/app/static/icon.ico'  # 여기에 아이콘 이미지 경로를 입력하세요

# 아이콘과 타이틀을 같은 줄에 배치
st.markdown(
    f"""
    <div style="display: flex; align-items: center;">
        <img src="{icon_image_path}" style="width:45px; margin-right:10px;">
        <h1 style="margin: 0;">Demo Dashboard Title</h1>
    </div>
    """,
    unsafe_allow_html=True
)

st.subheader('✅test sub header')
# st.text('test dataframe')
df = pd.read_csv('./설치장소_gis.csv',encoding='cp949')

with st.expander('Raw Data'):
    st.dataframe(df)

# Custom HTML and CSS for tooltip
tooltip_html = """
<style>
/* Container holding the metric and tooltip */
.metric-container {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
}

/* Style for the metric label with tooltip */
.metric-label {
    position: relative;
    display: block;
    margin-bottom: 3px; /* Adjust spacing between label and value */
}

/* Tooltip text */
.tooltip-text {
    visibility: hidden;
    width: 160px;
    background-color: black;
    color: #fff;
    text-align: center;
    border-radius: 6px;
    padding: 5px;
    position: absolute;
    z-index: 1;
    bottom: 125%;
    left: 50%;
    margin-left: -80px;
    opacity: 0;
    transition: opacity 0.3s, visibility 0.3s;
}

/* Show tooltip text on hover */
.metric-label:hover .tooltip-text {
    visibility: visible;
    opacity: 1;
}

/* Style for the metric value */
.metric-value {
    font-size: 20px; /* Adjust font size if needed */
}
</style>

<div class="metric-container">
    <div class="metric-label">
        test label
        <div class="tooltip-text">
            Tooltip text here
        </div>
    </div>
    <!-- Placeholder for the metric value -->
    <div class="metric-value">
        13515
    </div>
</div>
"""

# Display custom tooltip with metric label
st.markdown(tooltip_html, unsafe_allow_html=True)


# Metric 값 정의
# label = "Temperature"
# value = "72°F"
# delta = "+3°F"
#
# # HTML 및 CSS로 커스텀 Metric 만들기
# st.markdown(
#     f"""
#     <div style="
#         background-color: white;
#         border: 1px solid red;
#         border-radius: 5px;
#         padding: 10px;
#         text-align: center;
#     ">
#         <span style="font-size: 2rem; font-weight: bold;">{label}</span><br>
#         <span style="font-size: 1.5rem;">{value}</span><br>
#         <span style="font-size: 1rem; color: {'green' if delta.startswith('+') else 'red'};">{delta}</span>
#     </div>
#     """,
#     unsafe_allow_html=True
# )


# GPKG 파일 경로
gpkg_file_path = './korea_outline.gpkg'  # 여기에 GPKG 파일 경로를 입력하세요

# GeoDataFrame으로 GPKG 파일 읽기 (캐싱)
@st.cache_data
def load_gpkg(file_path):
    return gpd.read_file(file_path)

gdf = load_gpkg(gpkg_file_path)

# print(gdf)
# 지도 생성
m = folium.Map(location=[37.5665, 126.978], zoom_start=7\
               , tiles='CartoDB positron')  # 서울의 위도와 경도
# '''
# CartoDB Positron: tiles='CartoDB positron'
# CartoDB Dark Matter: tiles='CartoDB dark_matter'
# Stamen Terrain: tiles='Stamen Terrain'
# Stamen Toner: tiles='Stamen Toner'
# '''


# GeoDataFrame을 GeoJSON으로 변환하여 추가

# geojson_data = gdf.__geo_interface__

# Read the GEOJSON file\
@st.cache_data
def read_geojson():
    geojson_data = gpd.read_file('./output.geojson')
    return geojson_data

geojson_data = read_geojson()

# print("geojson_data")
# print(geojson_data)
folium.GeoJson(
    geojson_data,
    popup=folium.GeoJsonPopup(fields=['name', 'name_eng']),  # 팝업에 이름과 영어 이름 표시
    style_function=lambda x: {
        'fillColor': 'white',
        'color': 'black',
        'weight': 1,
        'fillOpacity': 0.5
    }
).add_to(m)

# # GeoDataFrame의 각 피처를 Folium 레이어로 추가
# for _, row in gdf.iterrows():
#     # 각 피처의 geometry를 가져옵니다.
#     geom = row['geometry']
#
#     # geometry의 타입에 따라 적절한 Folium 객체를 생성합니다.
#     if geom.geom_type == 'Polygon' or geom.geom_type == 'MultiPolygon':
#         folium.GeoJson(
#             geom,
#             popup=f"{row['name']} ({row['name_eng']})",  # 팝업에 이름과 영어 이름 표시
#             style_function=lambda x: {
#                 'fillColor': 'blue',
#                 'color': 'black',
#                 'weight': 1,
#                 'fillOpacity': 0.5
#             }
#         ).add_to(m)


# 마커 추가
# @st.cache_resource
def place_marker(map_object):
    for idx, row in df.iterrows():
        location  = (row['Y'],row['X'])
        # print(location)
        folium.Marker(
            location=location,
            popup=row['표준구주소'],
            # icon=folium.Icon(color='blue'),
            # icon = folium.Icon(color='blue')
        ).add_to(m)

# 초기화 상태 체크 및 마커 추가
if 'markers_added' not in st.session_state:
    place_marker(m)
    st.session_state.markers_added = True

# place_marker()
# Streamlit에 Folium 지도 표시
st_folium(m, width=700, height=500)