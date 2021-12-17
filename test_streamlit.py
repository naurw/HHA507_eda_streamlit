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
    hospital = pd.read_csv('/Users/William/Desktop/AHI_DataSci_507/Deployment_Streamlit/hospital_info.csv')
    return hospital

@st.cache
def load_inpatient():
    inpatient = pd.read_csv('/Users/William/Desktop/AHI_DataSci_507/Deployment_Streamlit/inpatient_2015.csv')
    return inpatient

@st.cache
def load_outpatient():
    outpatient = pd.read_csv('/Users/William/Desktop/AHI_DataSci_507/Deployment_Streamlit/outpatient_2015.csv')
    return outpatient


#Load the data:     
hospital = load_hospitals()
inpatient = load_inpatient()
outpatient = load_outpatient()

st.header('Hospital Data Preview')
st.dataframe(hospital_info)

st.header('Outpatient Data Preview')
st.dataframe(outpatient2015)

st.header('Inpatient Data Preview')
st.dataframe(inpatient2015)