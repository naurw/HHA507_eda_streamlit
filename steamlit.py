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
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import time


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

# =============================================================================
# Title
# =============================================================================

st.title('Overview of Hospital Performance and Payments in NY Inpatient and Outpatient Facilities in 2015')
st.markdown('By: William Ruan')
st.markdown('Last updated: December 15th, 2021')
st.markdown('The purpose of this exploratory analysis is to compare hospital performance across New York utilizing Python for programming and Streamlit for deployment. The variables used in this case study report includes mortality rate, safety of care, and patient experience. In addition, average total payments for providers in inpatient and outpatient facilities will be compared. This report will also provide a dive into the hospital performance of and total payments to: Stony Brook University Hospital, Maimonides Medical Center, and Mount Sinai Hospital.')

#Creating Menu to look at the datasets used in this dashboard
st.markdown('Three national-level datasets were used in this report. To review each dataset, click on the drop down bar below. However, please note that due to the number of observations within these dataset, loading time may take some time. Please give it a moment and take a sip of your favorite drink. :smile:')
selectbar = st.selectbox('Select Dataset', ("Hospital Experience", "Inpatient Payments", "Outpatient Payments"))


def get_dataset(selectbar):
    if selectbar == 'Hospital Experience':
        st.write(hospital)
    if selectbar == 'Inpatient Payments':
        st.write(inpatient)
    if selectbar == 'Outpatient Payments':
        st.write(outpatient)

st.write(get_dataset(selectbar))


# =============================================================================
# Hospitals in New York
# =============================================================================

st.markdown('---')
st.title('Hospitals in New York')
newyorkHospitals = hospital[hospital['state'] == 'NY'].sort_values('hospital_name')


nyHospitalTypes = newyorkHospitals['hospital_type'].value_counts().reset_index()
st.dataframe(nyHospitalTypes)
st.markdown('The table above indicates the number of different hospitals in New York, as based on the datasets used in this report. As seen within the chart, the majority of New York hospitals are acute care, followed by psychiatric.')

fig = px.pie(nyHospitalTypes, values='hospital_type', names='index')
st.plotly_chart(fig)
st.markdown('The pie chart above visualizes the distribution of the types of hospitals within New York. Counts of the hospitals can be found by hovering over the percentages.')

st.subheader('Map of NY Hospital Locations')
newyorkHospitals_gps = newyorkHospitals['location'].str.strip('()').str.split(' ', expand=True).rename(columns={0: 'Point', 1:'lon', 2:'lat'}) 	
newyorkHospitals_gps['lon'] = newyorkHospitals_gps['lon'].str.strip('(')
newyorkHospitals_gps = newyorkHospitals_gps.dropna()
newyorkHospitals_gps['lon'] = pd.to_numeric(newyorkHospitals_gps['lon'])
newyorkHospitals_gps['lat'] = pd.to_numeric(newyorkHospitals_gps['lat'])
st.map(newyorkHospitals_gps)
st.markdown('The interactive map above can be utilized to explore the locations of New York hospitals. Based on the map data, majority of the hospitals are within New York City.')

# =============================================================================
# Hospital Performance
# =============================================================================

st.markdown('---')
st.title('Hospital Performance')        
st.markdown('The focus in this section will be on comparing the hospital performance of Stony Brook University Hospital, Maimonides Medical Center, and Mount Sinai Hospital with their respective counties: Suffolk, Kings, and New York.')


suffolk = newyorkHospitals[newyorkHospitals['county_name']=='SUFFOLK']
suffolk = suffolk[['provider_id','hospital_name','city','state','county_name','hospital_type','mortality_national_comparison','safety_of_care_national_comparison','patient_experience_national_comparison']]

kings = newyorkHospitals[newyorkHospitals['county_name']=='KINGS']
kings = kings[['provider_id','hospital_name','city','state','county_name','hospital_type','mortality_national_comparison','safety_of_care_national_comparison','patient_experience_national_comparison']]

newyork = newyorkHospitals[newyorkHospitals['county_name']=='NEW YORK']
newyork = newyork[['provider_id','hospital_name','city','state','county_name','hospital_type','mortality_national_comparison','safety_of_care_national_comparison','patient_experience_national_comparison']]


# =============================================================================
# Suffolk County 
# =============================================================================

st.header('SUFFOLK COUNTY')

st.markdown('<font color=‘blue’>STONY BROOK UNIVERSITY HOSPITAL</font>', unsafe_allow_html=True)
st.markdown('The table below indicates hospital performance data for SUNY Stony Brook University Hospital. Please click on the drag bar to move to the left or right of this table. When compared at the national level, SBU Hospital is above average for mortality and safety of care. However, it is below the national average in patient experience. This could imply that improved safety of care does not necessarily decrease mortality rate in Stony Brook University Hospital. According to the dataset used and the pie charts below, most hospitals in Suffolk have an above average mortality rate. There is an equal amount of hospitals with above average and below average safety of care in Suffolk County. Most hospitals are below the national average in terms of patient experience. SBU Hospital follows the trends of most Suffolk County hospitals for mortality, safety of care, and patient experience.')

stony = newyorkHospitals.loc[newyorkHospitals['hospital_name'] == 'SUNY/STONY BROOK UNIVERSITY HOSPITAL']
stony = stony[['provider_id','hospital_name','county_name','hospital_type','mortality_national_comparison','safety_of_care_national_comparison','patient_experience_national_comparison']]
st.dataframe(stony)

st.markdown('<font color=‘blue’>SUFFOLK COUNTY MORTALITY</font>', unsafe_allow_html=True)
suffolk_mortality = suffolk['mortality_national_comparison'].value_counts().reset_index()
suf_mort_pie = px.pie(suffolk_mortality, values='mortality_national_comparison', names='index')
st.plotly_chart(suf_mort_pie)


st.markdown('<font color=‘blue’>SUFFOLK COUNTY SAFETY OF CARE</font>', unsafe_allow_html=True)
suffolk_safety = suffolk['safety_of_care_national_comparison'].value_counts().reset_index()
suf_safety_pie = px.pie(suffolk_safety, values='safety_of_care_national_comparison', names='index')
st.plotly_chart(suf_safety_pie)


st.markdown('<font color=‘blue’>SUFFOLK COUNTY PATIENT EXPERIENCE</font>', unsafe_allow_html=True)
suffolk_patient = suffolk['patient_experience_national_comparison'].value_counts().reset_index()
suffolk_patient_exp = px.pie(suffolk_patient, values='patient_experience_national_comparison', names='index')
st.plotly_chart(suffolk_patient_exp)


# =============================================================================
# Kings County 
# =============================================================================

st.header('KINGS COUNTY')

st.markdown('<font color=‘green’>MAIMONIDES MEDICAL CENTER</font>', unsafe_allow_html=True)
st.markdown('The table below indicates hospital performance data for Maimonides Medical Center. When compared at the national level, Maimonides Medical Center has: above average in mortality rate and below average in safety of care and patient experience. When compared to the rest of the hospitals in Kings County, Maimonides Medical Center is doing worse in terms of mortality rate. Most hospitals in this county have below the national average for safety of care and patient experience.')

maimonides = newyorkHospitals.loc[newyorkHospitals['hospital_name'] == 'MAIMONIDES MEDICAL CENTER']
maimonides = maimonides[['provider_id','hospital_name','county_name','hospital_type','mortality_national_comparison','safety_of_care_national_comparison','patient_experience_national_comparison']]
st.dataframe(maimonides)

kings_mortality = kings['mortality_national_comparison'].value_counts().reset_index()

st.markdown('<font color=‘green’>KINGS COUNTY MORTALITY</font>', unsafe_allow_html=True)
kings_mortality = kings['mortality_national_comparison'].value_counts().reset_index()
kings_mort_pie = px.pie(kings_mortality, values='mortality_national_comparison', names='index')
st.plotly_chart(kings_mort_pie)


st.markdown('<font color=‘green’>KINGS COUNTY SAFETY OF CARE</font>', unsafe_allow_html=True)
kings_safety = kings['safety_of_care_national_comparison'].value_counts().reset_index()
kings_safety_pie = px.pie(kings_safety, values='safety_of_care_national_comparison', names='index')
st.plotly_chart(kings_safety_pie)


st.markdown('<font color=‘green’>KINGS COUNTY PATIENT EXPERIENCE</font>', unsafe_allow_html=True)
kings_patient = kings['patient_experience_national_comparison'].value_counts().reset_index()
kings_patient_exp = px.pie(kings_patient, values='patient_experience_national_comparison', names='index')
st.plotly_chart(kings_patient_exp)


# =============================================================================
# New York County 
# =============================================================================
st.header('NEW YORK COUNTY')


st.markdown('<font color=‘orange’>MOUNT SINAI HOSPITAL</font>', unsafe_allow_html=True)
st.markdown('The table below indicates hospital performance data for Mount Sinai Hospital. When compared at the national level, Mount Sinai Hospital is above the national average for mortality and safety of care. However, it is below the national average for patient experience. In New York County, most hospitals are above average in terms of mortality rate and below average in terms of patient experience. However, Mount Sinai is doing better compared to other hospitals in New York County in terms of safety of care.')

sinai = newyorkHospitals.loc[newyorkHospitals['hospital_name'] == 'MOUNT SINAI HOSPITAL']
sinai = sinai[['provider_id','hospital_name','county_name','hospital_type','mortality_national_comparison','safety_of_care_national_comparison','patient_experience_national_comparison']]
st.dataframe(sinai)


ny_mortality = newyork['mortality_national_comparison'].value_counts().reset_index()

st.markdown('<font color=‘orange’>NEW YORK COUNTY MORTALITY</font>', unsafe_allow_html=True)
ny_mortality = newyork['mortality_national_comparison'].value_counts().reset_index()
ny_mort_pie = px.pie(ny_mortality, values='mortality_national_comparison', names='index')
st.plotly_chart(ny_mort_pie)


st.markdown('<font color=‘orange’>NEW YORK COUNTY SAFETY OF CARE</font>', unsafe_allow_html=True)
ny_safety = newyork['safety_of_care_national_comparison'].value_counts().reset_index()
ny_safety_pie = px.pie(ny_safety, values='safety_of_care_national_comparison', names='index')
st.plotly_chart(ny_safety_pie)


st.markdown('<font color=‘orange’>NEW YORK PATIENT EXPERIENCE</font>', unsafe_allow_html=True)
ny_patient = newyork['patient_experience_national_comparison'].value_counts().reset_index()
ny_patient_exp = px.pie(ny_patient, values='patient_experience_national_comparison', names='index')
st.plotly_chart(ny_patient_exp)



st.markdown('---')

# =============================================================================
# Inpatient
# =============================================================================
st.title('Inpatient Payments')

outpatient['provider_id'] = outpatient['provider_id'].astype(str)
outpatient['provider_id'].dtype

inpatient['provider_id'] = inpatient['provider_id'].astype(str)
inpatient['provider_id'].dtype

inpatientMerged = inpatient.merge(newyorkHospitals, how='left', on='provider_id')
inpatientMerged = inpatientMerged[inpatientMerged['hospital_name'].notna()]
nyInpatient = inpatientMerged[inpatientMerged['state'] == 'NY']
total_inpatient_count = sum(nyInpatient['total_discharges'])

st.markdown('Below are the total discharges for each type of diagnosis related group (DRG) in NY hospitals. The most discharges involve septicemia or sever sepsis, while the least discharges involve O.R. procedures for multiple significant trauma. The total number of discharges from inpatient hospitals in NY is 425742.')
##Common D/C 
common_discharges = nyInpatient.groupby('drg_definition')['total_discharges'].sum().reset_index()
common_discharges = common_discharges.sort_values('total_discharges', ascending=False)

top10 = common_discharges.head(10)
bottom10 = common_discharges.tail(10)

st.header('DRGs in Inpatient NY Hospitals')
st.dataframe(common_discharges)

col1, col2 = st.columns(2)

col1.header('Top 10 DRGs')
col1.dataframe(top10)

col2.header('Bottom 10 DRGs')
col2.dataframe(bottom10)


inpatient_3_hospitals = nyInpatient.loc[(nyInpatient['hospital_name']=='MOUNT SINAI HOSPITAL') | (nyInpatient['hospital_name']=='SUNY/STONY BROOK UNIVERSITY HOSPITAL') | (nyInpatient['hospital_name']=='MAIMONIDES MEDICAL CENTER')]
costs = inpatient_3_hospitals.groupby('hospital_name')['average_total_payments'].sum().reset_index()
costs['average_total_payments'] = costs['average_total_payments'].astype('int64')

costs_medicare = inpatient_3_hospitals.groupby('hospital_name')['average_medicare_payments'].sum().reset_index()
costs_medicare['average_medicare_payments'] = costs_medicare['average_medicare_payments'].astype('int64')
costs_sum = costs.merge(costs_medicare, how='left', left_on='hospital_name', right_on='hospital_name')
costs_sum['delta'] = costs_sum['average_total_payments'] - costs_sum['average_medicare_payments']
costs_sum = costs_sum.sort_values('average_total_payments', ascending=False)

st.header('Average Total Payments in Maimonides, Mount Sinai, and Stony Brook University Hospital')

bar1 = px.bar(costs_sum, x='hospital_name', y='average_total_payments', color='hospital_name')
bar1.update_layout(xaxis_tickangle=-45)
st.plotly_chart(bar1)

st.markdown('This bar graph above represents the average total payments for Maimonides Medical Center, Mount Sinai Hospital, and Stony Brook University Hospital. Mount Sinai Hospital has almost 2 times more total payments than Maimonides and about 1/4 times more total payments than SBU Hospital.')

st.header("Hospital Average Payments")
st.dataframe(costs_sum)
st.markdown('The table above showcases the average total payments, average Medicare payments, and non-Medicare payments for the hospitals of interest. Mount Sinai has the largest non-Medicare total payment compared to Maimonides and Stony Brook.')


costs_condition_hospital = inpatient_3_hospitals.groupby(['hospital_name', 'drg_definition'])['average_total_payments'].sum().reset_index()
st.header("Costs by Condition and Hospital - Average Total Payments")
st.dataframe(costs_condition_hospital)

st.markdown('The table above showcases the average total payments by diagnosis related groups (DRGs) and hospital. The highest total payment for Maimonides Medical Center and Stony Brook University Hospital is for tracheostomy procedures. The highest total payment for Mount Sinai Hospital is for heart transplants. However, it is also noteworthy that the second highest payment in Mount Sinai also goes to tracheostomy procedures.')

st.markdown('---')



# =============================================================================
# Outpatient Payments
# =============================================================================
st.title('Outpatient Payments')

outpatientMerged = outpatient.merge(newyorkHospitals, how='left', on='provider_id')
outpatientMerged = outpatientMerged[outpatientMerged['hospital_name'].notna()]
nyOutpatient = outpatientMerged[outpatientMerged['state'] == 'NY']
total_outpatient_count = sum(nyOutpatient['outpatient_services'])
print(total_outpatient_count) #1865023
st.markdown('Below you will find the total number of patient services by APC code in NY outpatient facilities. The top 3 most utilized services are hospital clinic visits, level 1 echocardiogram without contrast, and level III diagnostic and screening ultrasound. On the other hand, the 3 least utilized services includes level III endoscopy upper airway, level II noninvasion physiologic studies, and level IV endoscopy upper airway. The total amount of outpatient services is 1865023.')

common_services = nyOutpatient.groupby('apc')['outpatient_services'].sum().reset_index()
common_services = common_services.sort_values('outpatient_services', ascending=False)

top10 = common_services.head(10)
bottom10 = common_services.tail(10)

st.header('APCs in Outpatient NY Facilities')
st.dataframe(common_services)

col1, col2 = st.columns(2)

col1.header('Top 10 APCs')
col1.dataframe(top10)

col2.header('Bottom 10 APCs')
col2.dataframe(bottom10)


#Drilling down to 3 facilities of interest
outpatient_3_facilities = nyOutpatient.loc[(nyOutpatient['hospital_name']=='MOUNT SINAI HOSPITAL') | (nyOutpatient['hospital_name']=='SUNY/STONY BROOK UNIVERSITY HOSPITAL') | (nyOutpatient['hospital_name']=='MAIMONIDES MEDICAL CENTER')]

#Outpatient Average Payments
st.header('Average Total Payments in Maimonides, Mount Sinai, and Stony Brook University Hospital for Outpatient Services')

outpatient_sum = outpatient_3_facilities.groupby('hospital_name')['average_total_payments'].sum().reset_index()
outpatient_sum['average_total_payments'] = outpatient_sum['average_total_payments'].astype('int64')
outpatient_sum = outpatient_sum.sort_values('average_total_payments', ascending=False)

bar2 = px.bar(outpatient_sum, x='hospital_name', y='average_total_payments', color='hospital_name')
bar2.update_layout(xaxis_tickangle=-45)
st.plotly_chart(bar2)

st.markdown('This bar graph above represents the average total payments for Maimonides Medical Center, Mount Sinai Hospital, and Stony Brook University Hospital for outpatient services. Mount Sinai Hospital has about 2 times more total payments than Maimonides and almost 1/7 times more total payments than SBU Hospital.')

st.header("Outpatient Average Payments")
st.dataframe(outpatient_sum)
st.markdown('The table above showcases the average total payments for the facilities of interest. Likewise, Mount Sinai has the highest average total payments for outpatient services when compared to Maimonides and Stony Brook.')

#Costs by Condition and Hospital / Average Total Payments
costs_service_outpatient = outpatient_3_facilities.groupby(['hospital_name', 'apc'])['average_total_payments'].sum().reset_index().sort_values('average_total_payments', ascending=False)
st.header("Costs by Condition and Outpatient Facility - Average Total Payments")
st.dataframe(costs_service_outpatient)


st.markdown('The table above showcases the average total payments by APC and facility. The highest total payment for Mount Sinai and SBU Hospital is for level IV endoscopy for the upper airway. However, the highest total payment for Maimonides is for level II cardiac imaging.')

st.markdown('---')