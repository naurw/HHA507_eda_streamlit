#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 15 13:53:48 2021

@author: William
"""

#conda install -c conda-forge streamlit
#conda install -c plotly plotly
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

@st.cache
def load_hospitals():
    hospital = pd.read_csv('https://raw.githubusercontent.com/hantswilliams/AHI_STATS_507/main/Week13_Summary/output/df_hospital_2.csv')
    return hospital

@st.cache
def load_outpatient():
    outpatient = pd.read_csv('https://raw.githubusercontent.com/hantswilliams/AHI_STATS_507/main/Week13_Summary/output/df_outpatient_2.csv')
    return outpatient

@st.cache
def load_inpatient():
    inpatient = pd.read_csv('https://raw.githubusercontent.com/hantswilliams/AHI_STATS_507/main/Week13_Summary/output/df_inpatient_2.csv')
    return inpatient

#Load the data:     
hospital = load_hospitals()
inpatient = load_inpatient()
outpatient = load_outpatient()

st.header('Hospital Data Preview')
st.dataframe(hospital)

st.header('Outpatient Data Preview')
st.dataframe(outpatient)

st.header('Inpatient Data Preview')
st.dataframe(inpatient)