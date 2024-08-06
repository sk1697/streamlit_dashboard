import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title='test dashboard',page_icon='./icon.ico',layout='wide')

st.title('Test Title')


st.subheader('✅test sub header')
st.text('test dataframe')
df = pd.read_csv('./2024년도_학년별·학급별 학생수(초)_경상북도교육청.csv')

st.write(df)