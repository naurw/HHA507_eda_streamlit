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


st.title('A Deep Dive on Hospital Performance and Payments in NY Inpatient and Outpatient Facilities')
st.markdown('By: William Ruan')
st.markdown('Last updated: :smile:')
st.markdown('The purpose of this exploratory analysis is to compare hospital performance across New York utilizing Python for programming and Streamlit for deployment. The variables used in this case study report includes mortality rate, safety of care, and patient experience. In addition, average total payments for providers in inpatient and outpatient facilities will be compared. This report will also provide a dive into the hospital performance of and total payments to: Stony Brook University Hospital, Maimonides Medical Center, and Mount Sinai Hospital.')

#Creating Menu to look at the datasets used in this dashboard
st.markdown('Three national-level datasets were used in this report. To review each dataset, please click on the select bar below. However, please note that due to the number of observations within these dataset, loading time may take some time. Please give it a moment and take a sip of your favorite drink. :smile:')
selectbar = st.selectbox('Select Dataset', ("Hospital Experience", "Inpatient Payments", "Outpatient Payments"))


def get_dataset(selectbar):
    if selectbar == 'Hospital Experience':
        st.write(hospital)
    if selectbar == 'Inpatient Payments':
        st.write(inpatient)
    if selectbar == 'Outpatient Payments':
        st.write(outpatient)

st.write(get_dataset(selectbar))