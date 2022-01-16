#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 27 16:10:15 2021

@author: William
"""

''' Modified variant of edaCodes.py with codes that are found on Streamlit '''
''' Purpose of this file is to replicate tedious codes via rudimentary logic functions and explore alternatives to make the codes more elegant/easier reference '''
''' Pandas and numpy have boolean indexing capabilties built in so generating nested functions for filtering is usually NOT AS EFFICIENT '''
''' Analysis + visuals can be found in the bottom of this file '''



import pandas as pd 
import glob
import os
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
#conda install -c conda-forge geopandas
#conda install -c conda-forge fiona shapely pyproj libgdal



# =============================================================================
# Loading dataframes
# =============================================================================

path = os.getcwd()
print('Current default local path is:', path)
csv_files = glob.glob(os.path.join(path, 'Desktop/AHI_DataSci_507/Deployment_Streamlit', '*.csv'))
csv_files

print('The total number of csv files that will be analyzed are ', len(csv_files), '.', sep='')
print('File paths/names are:', csv_files)

csvList = []
for i in csv_files: 
    df = pd.read_csv(i)
    csvList.append(df)
    
    print('Location:', i)
    print('File Name:', i.split('\\')[-1])
    print('Content')
    display(df)

df = pd.concat(csvList)

inpatient = pd.DataFrame(csvList[0])
outpatient = pd.DataFrame(csvList[1])
hospital = pd.DataFrame(csvList[2])
print('The total number of rows within hospital is ', len(hospital), '.', sep='') 
print("The total number of rows within the inpatient is {}.".format(len(inpatient)))
print('The total number of rows within the outpatient is {}.'.format(len(outpatient)))
print('The total length of rows in the concatenated df should be {}.'.format(len(hospital) + len(inpatient) + len(outpatient)),
      'Confirm with: {}.'.format(len(df)))

# =============================================================================
# Option 2 (Purposely redundant with functions; not necessary to load)
# =============================================================================
# =============================================================================
# 
# def load_hospitals():
#     hospital = pd.read_csv('https://raw.githubusercontent.com/hantswilliams/AHI_STATS_507/main/Week13_Summary/output/df_hospital_2.csv')
#     return hospital
# 
# def load_outpatient():
#     outpatient = pd.read_csv('https://raw.githubusercontent.com/hantswilliams/AHI_STATS_507/main/Week13_Summary/output/df_outpatient_2.csv')
#     return outpatient
# 
# def load_inpatient():
#     inpatient = pd.read_csv('https://raw.githubusercontent.com/hantswilliams/AHI_STATS_507/main/Week13_Summary/output/df_inpatient_2.csv')
#     return inpatient
# 
# hospital = load_hospitals()
# inpatient = load_outpatient()
# outpatient = load_inpatient()
#
# =============================================================================


# =============================================================================
# Initial analysis and cleaning of dataframes 
# =============================================================================

def c(i):
    out1 = i.head(5) 
    out2 = i.tail(5)
    out3 = i.sample(20)
    out4 = i.info()
    out5 = i.isnull().sum()
    return ({'head': out1, 'tail': out2, 'samp': out3, 'info': out4, 'null': out5})

df_sample = c(df)['samp']
inpatient_sample = c(inpatient)['samp']
outpatient_sample = c(outpatient)['samp']
hospital_sample = c(hospital)['samp']

c(outpatient)['info']
outpatient['provider_id'] = outpatient['provider_id'].astype(str)
outpatient['provider_id'].dtype
c(outpatient)['null']
print('Within the dataframe outpatient, there are {} unique providers.'.format(outpatient['provider_id'].nunique()))
print('There are a total of {} providers within outpatient, which is due to the number of APC services provided per provider.'.format(outpatient.provider_id.count()))

c(inpatient)['info']
inpatient['provider_id'] = inpatient['provider_id'].astype(str)
inpatient['provider_id'].dtype
c(inpatient)['null']
print('Within the dataframe inpatient, there are {} unique providers.'.format(inpatient['provider_id'].nunique()))
print('There are a total of {} providers within inpatient, which is due to the number of DRG services provided per provider.'.format(inpatient.provider_id.count()))

c(hospital)['info']
c(hospital)['null']
hospital.hospital_name.nunique()
hospital.hospital_name.value_counts().sum()
print('Within the dataframe hospital, there are a total of ', hospital.hospital_name.nunique(), ' unique hospitals out of ', len(hospital.hospital_name), '.', sep='')
print('Some of the repeating hospital names are:', hospital.hospital_name.value_counts().head(20))
print('Hospitals with repeating names such as Memorial Hospital have ', len(hospital[hospital['hospital_name'] == 'MEMORIAL HOSPITAL']),
      ' branches across several regions', '.', sep='')

hospital.hospital_ownership.value_counts().sort_values(ascending=False)
hGov = ['Government - Federal', 'Government - State', 'Government - Local', 'Government - Hospital District or Authority', 'Department of Defense']
hVol = ['Voluntary non-profit - Private', 'Voluntary non-profit - Other', 'Voluntary non-profit - Church']
hInd = ['Tribal', 'Physician', 'Proprietary']

def owner(i):
    output1 = i.loc[i['hospital_ownership'].isin(hGov), 'hospital_ownership'] = 'Government'
    output2 = i.loc[i['hospital_ownership'].isin(hVol), 'hospital_ownership'] = 'Voluntary'
    output3 = i.loc[i['hospital_ownership'].isin(hInd), 'hospital_ownership'] = 'Independent'
    return ({'gov': output1, 'vol': output2, 'ind': output3})

owner(hospital)['gov']
owner(hospital)['vol']
owner(hospital)['ind']
print('The most common type of hospital is Voluntary Hospitals, as seen below:', hospital['hospital_ownership'].value_counts())
print('The most common type of hospital is Acute Care Hospitals, as seen below:', hospital.hospital_type.value_counts())
acuteVoluntary = hospital.loc[(hospital['hospital_ownership'] == 'Voluntary') & (hospital['hospital_type'] == 'Acute Care Hospitals') & (hospital['state'] == 'NY')]
## Move this to New York Section later 

hospital[['Point', 'Longitude', 'Latitude']] = hospital['location'].str.strip('()').str.split(' ', expand=True).rename(columns={0: 'Point', 1:'Longitude', 2:'Latitude'}) 
hospital['Longitude'] = hospital['Longitude'].str.strip('(')
hospital.info()
hospital['Longitude'] = hospital['Longitude'].astype(float)
hospital['Latitude'] = pd.to_numeric(hospital['Latitude'])
hospital.drop(['location'], axis =1, inplace=True)

''' 
to_numeric() - provides functionality to safely convert non-numeric types (e.g. strings) to a suitable numeric type. (See also to_datetime() and to_timedelta().)

astype() - convert (almost) any type to (almost) any other type (even if it's not necessarily sensible to do so). Also allows you to convert to categorial types (very useful).

infer_objects() - a utility method to convert object columns holding Python objects to a pandas type if possible.

convert_dtypes() - convert DataFrame columns to the "best possible" dtype that supports pd.NA (pandas' object to indicate a missing value).
'''


# =============================================================================
# Pie chart, where the slices will be ordered and plotted counter-clockwise:
# =============================================================================
# =============================================================================
# labels = 'Frogs', 'Hogs', 'Dogs', 'Logs'
# sizes = [15, 30, 45, 10]
# explode = (0, 0.1, 0, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')
# 
# fig1, ax1 = plt.subplots()
# ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
#         shadow=True, startangle=90)
# ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
# 
# plt.show()
# =============================================================================

# =============================================================================
# Map 
# =============================================================================

newyorkHospitals = hospital[hospital['state'] == 'NY'].sort_values('hospital_name') 

nyHospitalTypes = newyorkHospitals['hospital_type'].value_counts().reset_index()
#nyHospitalTypes = newyorkHospitals.hospital_type.value_counts().to_frame().reset_index() <-- longer way to convert a series into a dataframe with the addition of .to_frame()

fig = px.pie(nyHospitalTypes, values='hospital_type', names='index')
fig.show()

''' Separate dataframe with only coordinates for mapping purposes and to keep relevant information '''
nyMap = newyorkHospitals[['Point', 'Longitude', 'Latitude']]
nyMap = nyMap.dropna()
nyMap.info()

g_nyMap = geopandas.GeoDataFrame(nyMap, geometry=geopandas.points_from_xy(nyMap.Longitude, nyMap.Latitude))

geopandas.datasets.available
world = geopandas.read_file(geopandas.datasets.get_path('naturalearth_lowres'))
newyork = geopandas.read_file(geopandas.datasets.get_path('nybb'))
cities = geopandas.read_file(geopandas.datasets.get_path('naturalearth_cities'))

ax = world[world.continent == 'United States of America'].plot(color='white', edgecolor='black')
g_nyMap.plot(ax=ax, color='red')
plt.show()

ax1 = newyork.plot(color= 'Blue', edgecolor= 'Black') 
g_nyMap.plot(ax1=ax1, color = 'red')
plt.show()

# =============================================================================
# New York State 
# =============================================================================
newyorkHospitals = hospital[hospital['state'] == 'NY']
newyorkHospitals['hospital_type'].value_counts()
newyorkHospitals['hospital_name'].value_counts()
newyorkHospitals['hospital_name'].value_counts().sum()
newyorkHospitals.hospital_name.nunique()

nycCounty = ['KINGS', 'QUEENS', 'NEW YORK', 'BRONX', 'RICHMOND']
nyc = newyorkHospitals[newyorkHospitals['county_name'].isin(nycCounty)]
print('The total number of hospitals within New York is:', len(nyc))
kings = newyorkHospitals[newyorkHospitals['county_name'] == 'KINGS']
manhattan = newyorkHospitals[newyorkHospitals['county_name'] == 'NEW YORK']
suffolk = newyorkHospitals[newyorkHospitals['county_name'] == 'SUFFOLK']
print('There are a total of', len(kings), 'hospitals within Kings County (Brooklyn), New York')
print('There are a total of', len(manhattan), 'hospitals within New York County (Manhattan/NewYork), New York')
print('There are a total of', len(suffolk), 'hospitals within Suffolk County (Long Island), New York')

# =============================================================================
# Stony Brook University Hospital 
# =============================================================================
inpatientMerged = inpatient.merge(newyorkHospitals, how= 'left', on= 'provider_id' )
inpatientMergedSample = c(inpatientMerged)['samp']
cleanMerge = inpatientMerged[inpatientMerged['hospital_name'].notna()]

sbuInpatient = cleanMerge.loc[cleanMerge['hospital_name'] == 'SUNY/STONY BROOK UNIVERSITY HOSPITAL']
sbuInpatient.info()
sbuInpatientCleaned = sbuInpatient[['provider_id', 'drg_definition', 'total_discharges', 'average_covered_charges', 'average_total_payments', 'average_medicare_payments']]
#charges = pd.DataFrame(sbuInpatientCleaned.groupby('drg_definition')['average_covered_charges'])

def drg(i): 
    avgCharges = i[['drg_definition', 'average_covered_charges']].sort_values(by='average_covered_charges', ascending=False)
    avgPayments = i[['drg_definition', 'average_total_payments']].sort_values(by='average_total_payments', ascending= False)
    avgMedicare = i[['drg_definition', 'average_medicare_payments']].sort_values(by= 'average_medicare_payments', ascending= False)
    avgDischarges = i[['drg_definition', 'total_discharges']].sort_values(by= 'total_discharges', ascending= False)
    return ({'chrg': avgCharges, 'pay': avgPayments, 'medi': avgMedicare, 'dchrg': avgDischarges})

sbuCharges = drg(sbuInpatient)['chrg']
sbuPayments = drg(sbuInpatient)['pay']
sbuMedicare = drg(sbuInpatient)['medi']
sbuDischarges = drg(sbuInpatient)['dchrg']
print('The sum of average total covered charges within SBU hospital is $', sbuInpatient.average_covered_charges.sum())
print('The sum of total inpatient discharges within SBU hospital is', sbuInpatient.total_discharges.sum())
print('The sum of average total payments within SBU hospital is $', sbuInpatient.average_total_payments.sum())
print('The sum of average medicare payments within SBU hospital is $', sbuInpatient.average_medicare_payments.sum())

c(sbuCharges)['head']
c(sbuCharges)['tail']
c(sbuPayments)['head']
c(sbuPayments)['tail']
c(sbuMedicare)['head']
c(sbuMedicare)['tail']
c(sbuDischarges)['head']
c(sbuDischarges)['tail']
# =============================================================================
# From this analysis of inpatient visits within Stony Brook Hospital:
#    - ECMO OR TRACH W MV >96 HRS OR PDX EXC FACE, MOUTH & NECK W MAJ O.R. is the MOST EXPENSIVE across multiple cost categories 
#    - RENAL FAILURE W/O CC/MCC or CARDIAC ARRHYTHMIA & CONDUCTION DISORDERS W/O CC/MCC are the LEAST EXPENSIVE depending on the cost categories chosen
#    - SEPTICEMIA OR SEVERE SEPSIS W/O MV 96+ HOURS W MCC is the MOST COMMON diagnosis group for discharges 
#    - There are several UNCOMMON discharges which can be seen above 
# =============================================================================

outpatientMerged = outpatient.merge(newyorkHospitals, how= 'left', on= 'provider_id')
outpatientMergedSample = outpatientMerged.sample(100)
cleanMerge2 = outpatientMerged[outpatientMerged['hospital_name'].notna()]

sbuOutpatient = cleanMerge2.loc[cleanMerge2['hospital_name'] == 'SUNY/STONY BROOK UNIVERSITY HOSPITAL']
sbuOutpatient.info()
sbuOutpatientCleaned = sbuOutpatient[['provider_id', 'apc', 'outpatient_services', 'average_estimated_submitted_charges', 'average_total_payments']]
#charges2 = pd.DataFrame(sbuOutpatientCleaned.groupby('apc')['average_estimated_submitted_charges'])

def apc(i): 
    avgSubCharges = i[['apc', 'average_estimated_submitted_charges']].sort_values(by='average_estimated_submitted_charges', ascending=False)
    avgTotalPayments = i[['apc', 'average_total_payments']].sort_values(by='average_total_payments', ascending= False)
    avgServices = i[['apc', 'outpatient_services']].sort_values(by= 'outpatient_services', ascending= False)
    return ({'chrg': avgSubCharges, 'pay': avgTotalPayments, 'serv': avgServices})

sbuOutpatientCharges = apc(sbuOutpatient)['chrg']
sbuOutpatientPayments = apc(sbuOutpatient)['pay']
sbuOutpatientServices = apc(sbuOutpatient)['serv']
print('The sum of all outpatient services within SBU hospital is', sbuOutpatient.outpatient_services.sum())
print('The sum of average estimated submitted charges is $', sbuOutpatient.average_estimated_submitted_charges.sum().round(2))
print('The sum of average total payments is $', sbuOutpatient.average_total_payments.sum().round(2))

sbuOutpatientCharges.head(5).round(2)
sbuOutpatientPayments.head(5).round(2)
sbuOutpatientServices.head(5).round(2)
# =============================================================================
# For this analysis of outpatient visits within Stony Brook Hospital: 
#    - Level IV Endoscopy Upper Airway is the MOST EXPENSIVE across multiple cost categories
#    - Level I Echocardiogram Without Contrast is the MOST COMMON outpatient service performed 
# =============================================================================

# =============================================================================
# New York's Hospitals based on overall ratings/national comparisons
# =============================================================================

print('These are all the hospitals grouped by ratings:', newyorkHospitals.groupby('hospital_overall_rating')['hospital_name'].count())

ratings = ['1', '2', '3', '4', '5']
high = ['4', '5']
low = ['1','2']
mid = ['3']
'''
In case there is confusion with the reason behind using strings instead of integers: 

                newyorkHospitals.hospital_overall_rating.astype(int)
                    ValueError: invalid literal for int() with base 10: 'Not Available'
                newyorkHospitals.hospital_overall_rating.dtype
                    dtype('O')

Solution: 
    - 1) replace 'Not Available' (reason of this error) to NaNs and subsequently using notna() to return rows that are not NaNs for the astype(int) to work 
    - 2) replace values with category codes to keep the Not Available but favored the solution below
    - 3) change numeric values within the array into strings to retain 'Not Available' for future data exploration 
'''

nyRatings = newyorkHospitals[newyorkHospitals['hospital_overall_rating'].isin(ratings)]
nyRatings = newyorkHospitals[ratingsFilter(newyorkHospitals.hospital_overall_rating)['Ratings']]
nyRatingsHospital = nyRatings[['hospital_overall_rating', 'hospital_name']]
nyBest = newyorkHospitals[newyorkHospitals['hospital_overall_rating'].isin(high)]
c(nyBest)['null']

def cleaned (i):
    removeAll = i.loc[:, ~i.columns.isin(['hospital_overall_rating_footnote', 'mortality_national_comparison_footnote', 'safety_of_care_national_comparison_footnote', 
                                    'readmission_national_comparison_footnote', 'patient_experience_national_comparison_footnote', 'effectiveness_of_care_national_comparison_footnote', 
                                    'timeliness_of_care_national_comparison_footnote', 'efficient_use_of_medical_imaging_national_comparison_footnote'])]
    five = i.loc[(i['hospital_overall_rating'] == '5')]
    three = i.loc[(i['hospital_overall_rating'] == '3')]
    one = i.loc[(i['hospital_overall_rating'] == '1')]
    compare = i[['provider_id', 'hospital_name', 'mortality_national_comparison', 'safety_of_care_national_comparison', 'readmission_national_comparison', 
                                    'patient_experience_national_comparison', 'effectiveness_of_care_national_comparison', 'timeliness_of_care_national_comparison', 
                                    'efficient_use_of_medical_imaging_national_comparison']]
    return ({'none': removeAll, '5': five, '3': three, '1': one, 'comp': compare})

nyBestCleaned = cleaned(nyBest)['none']
print('There are more hospitals (18) within New York State with a rating of 4 as seen below:', nyBestCleaned['hospital_overall_rating'].value_counts())
print('There are more acute care hospitals (19) within New York State with a rating of 4 or higher as seen below:', nyBestCleaned['hospital_type'].value_counts())
print('There are more voluntary or nonprofit (20) hospitals within New York State with a rating of 4 or higher as seen below:', nyBestCleaned['hospital_ownership'].value_counts())
nyBestCleaned['county_name'].value_counts().head(5)
nyBestCleaned['mortality_national_comparison'].value_counts()

len(nyBestCleaned)
nyBest3 = cleaned(nyBestCleaned)['5']
nyBest3.info()
nyBest3Comparison = cleaned(nyBest3)['comp']
nyBest2 = nyBestCleaned.loc[(nyBestCleaned['hospital_overall_rating'] == '5') & (nyBestCleaned['mortality_national_comparison'] != 'Not Available')]
nyBest2Comparison = cleaned(nyBest2)['comp']

nyWorst = newyorkHospitals[ratingsFilter(newyorkHospitals.hospital_overall_rating)['Low']]
nyWorstCleaned = cleaned(nyWorst)['none']
print('There are more hospitals (46) within New York State with a rating of 1 as seen below:', nyWorstCleaned.hospital_overall_rating.value_counts())
print('All hospitals are acute care (81) within New York State with a rating of 2 or lower as seen below:', nyWorstCleaned.hospital_type.value_counts()
print('There are more voluntary or nonprofit (66) hospitals within New York State with a rating of 2 or lower as seen below:', nyWorstCleaned.hospital_ownership.value_counts())
nyWorstCleaned.county_name.value_counts().head(3)

len(nyWorstCleaned)
nyWorst46 = cleaned(nyWorstCleaned)['1']
nycWorst23 = nyWorstCleaned.loc[(nyWorstCleaned['hospital_overall_rating'] == '1') & (nyWorstCleaned['county_name'].isin(nycCounty))]
nycWorst23Comparison = cleaned(nycWorst23)['comp']
nycWorst23.effectiveness_of_care_national_comparison.value_counts()

nycBelowEffectiveness = nycWorst23[nycWorst23['effectiveness_of_care_national_comparison'] == 'Below the national average']
nycBelowEffectiveness[['hospital_name']]

# =============================================================================
# New York State and New York City Hospitals based on inpatient data  
# =============================================================================
nyBestMerged = inpatient.merge(nyBestCleaned, how='left', on='provider_id')
nyBestMerged = nyBestMerged[nyBestMerged['hospital_name'].notna()]

def nyDrg (i):
    ny_avgDischarges = i[['hospital_name', 'city', 'county_name', 'drg_definition', 'total_discharges']].sort_values(by= 'total_discharges', ascending= False)
    ny_avgCharges = i[['hospital_name', 'city', 'county_name', 'drg_definition', 'average_covered_charges']].sort_values(by= 'average_covered_charges', ascending= False)
    ny_avgPayments = i[['hospital_name', 'city', 'county_name', 'drg_definition', 'average_total_payments']].sort_values(by= 'average_total_payments', ascending= False)
    ny_avgMedicare = i[['hospital_name', 'city', 'county_name', 'drg_definition', 'average_medicare_payments']].sort_values(by= 'average_medicare_payments', ascending= False)
    return ({'nydis': ny_avgDischarges})

nyDischarges = nyBestMerged[['hospital_name', 'city', 'county_name', 'drg_definition', 'total_discharges']].sort_values(by= 'total_discharges', ascending= False)
nyDischarges.head(3) 

nyCharges = nyBestMerged[['hospital_name', 'city', 'county_name', 'drg_definition', 'average_covered_charges']].sort_values(by= 'average_covered_charges', ascending= False)
nyCharges.head(3)

nyPayments = nyBestMerged[['hospital_name', 'city', 'county_name', 'drg_definition', 'average_total_payments']].sort_values(by= 'average_total_payments', ascending= False)
nyPayments.head(3)

nyMedicare = nyBestMerged[['hospital_name', 'city', 'county_name', 'drg_definition', 'average_medicare_payments']].sort_values(by= 'average_medicare_payments', ascending= False)
nyMedicare.head(3)

nyBestMerged.total_discharges.sum()

nyBest3_inpatient = nyBestMerged.loc[(nyBestMerged['hospital_overall_rating'] == '5')]
nyBest3_inpatient.groupby('hospital_name')['total_discharges'].sum().sort_values()

nyBest3_inpatient.groupby('hospital_name')['average_total_payments'].sum().sort_values()

nyBest3_inpatient.groupby('hospital_name')['average_medicare_payments'].sum().sort_values()

nyBest3_inpatient.groupby('hospital_name')['average_covered_charges'].sum()

nyBest3_inpatient.total_discharges.sum()

                    
nycBestMerged = nyBestMerged[nyBestMerged['county_name'].isin(nycCounty)]
nycBestMerged.info()
nycDischarges = nycBestMerged[['hospital_name', 'drg_definition', 'total_discharges']].sort_values(by= 'total_discharges', ascending= False)
nycDischarges.head(3) 

nycCharges = nycBestMerged[['hospital_name', 'drg_definition', 'average_covered_charges']].sort_values(by= 'average_covered_charges', ascending= False)
nycCharges.head(3)

nycPayments = nycBestMerged[['hospital_name', 'drg_definition', 'average_total_payments']].sort_values(by= 'average_total_payments', ascending= False)
nycPayments.head(3)

nycMedicare = nycBestMerged[['hospital_name', 'drg_definition', 'average_medicare_payments']].sort_values(by= 'average_medicare_payments', ascending= False)
nycMedicare.head(3)

nycBestMerged.total_discharges.sum()

nyWorstMerged = inpatient.merge(nyWorstCleaned, how='left', on='provider_id')
nyWorstMerged = nyWorstMerged[nyWorstMerged['hospital_name'].notna()]
nyWorstDischarges = nyWorstMerged[['hospital_name', 'city', 'county_name', 'drg_definition', 'total_discharges']].sort_values(by= 'total_discharges', ascending= False)
nyWorstDischarges.head(3) 
nyWorstCharges = nyWorstMerged[['hospital_name', 'city', 'county_name', 'drg_definition', 'average_covered_charges']].sort_values(by= 'average_covered_charges', ascending= False)
nyWorstCharges.head(3)
nyWorstPayments = nyWorstMerged[['hospital_name', 'city', 'county_name', 'drg_definition', 'average_total_payments']].sort_values(by= 'average_total_payments', ascending= False)
nyWorstPayments.head(3)
nyWorstMedicare = nyWorstMerged[['hospital_name', 'city', 'county_name', 'drg_definition', 'average_medicare_payments']].sort_values(by= 'average_medicare_payments', ascending= False)
nyWorstMedicare.head(3)
nyWorst_inpatient = nyWorstMerged.loc[(nyWorstMerged['hospital_overall_rating'] == '1')]
nyWorst_inpatient.groupby('hospital_name')['total_discharges'].sum().sort_values()
nyWorst_inpatient.total_discharges.sum()

nycWorstMerged = nyWorstMerged[nyWorstMerged['county_name'].isin(nycCounty)]
nycWorstMerged.info()
nycWorstDischarges = nycWorstMerged[['hospital_name', 'drg_definition', 'total_discharges']].sort_values(by= 'total_discharges', ascending= False)
nycWorstDischarges.head(3) 
nycWorstCharges = nycWorstMerged[['hospital_name', 'drg_definition', 'average_covered_charges']].sort_values(by= 'average_covered_charges', ascending= False)
nycWorstCharges.head(3)
nycWorstPayments = nycWorstMerged[['hospital_name', 'drg_definition', 'average_total_payments']].sort_values(by= 'average_total_payments', ascending= False)
nycWorstPayments.head(3)
nycWorstMedicare = nycWorstMerged[['hospital_name', 'drg_definition', 'average_medicare_payments']].sort_values(by= 'average_medicare_payments', ascending= False)
nycWorstMedicare.head(3)

nyBestOutpatientMerged = outpatient.merge(nyBestMerged, how='left', on='provider_id')
nyBestOutpatientMerged = nyBestOutpatientMerged[nyBestOutpatientMerged['hospital_name'].notna()]
nyBestOutpatientServices = nyBestOutpatientMerged[['hospital_name', 'city', 'county_name', 'apc', 'outpatient_services']].sort_values(by= 'outpatient_services', ascending= False)
nyBestOutpatientServices.head(3) 
nyBestOutpatientCharges = nyBestOutpatientMerged[['hospital_name', 'city', 'county_name', 'apc', 'average_estimated_submitted_charges']].sort_values(by= 'average_estimated_submitted_charges', ascending= False)
nyBestOutpatientCharges.head(3)
nyBestOutpatientPayments = nyBestOutpatientMerged[['hospital_name', 'city', 'county_name', 'apc', 'average_total_payments_y']].sort_values(by= 'average_total_payments_y', ascending= False)
nyBestOutpatientPayments.head(3)
nyBest_outpatient = nyBestOutpatientMerged.loc[(nyBestOutpatientMerged['hospital_overall_rating'] == '5')]
nyBest_outpatient.groupby('hospital_name')['outpatient_services'].sum().sort_values()
nyBest_outpatient.outpatient_services.sum()

nyWorstOutpatientMerged = outpatient.merge(nyWorstCleaned, how='left', on='provider_id')
nyWorstOutpatientMerged = nyWorstOutpatientMerged[nyWorstOutpatientMerged['hospital_name'].notna()]
nyWorstOutpatientServices = nyWorstOutpatientMerged[['hospital_name', 'city', 'county_name', 'apc', 'outpatient_services']].sort_values(by= 'outpatient_services', ascending= False)
nyWorstOutpatientServices.head(3) 
nyWorstOutpatientCharges = nyWorstOutpatientMerged[['hospital_name', 'city', 'county_name', 'apc', 'average_estimated_submitted_charges']].sort_values(by= 'average_estimated_submitted_charges', ascending= False)
nyWorstOutpatientCharges.head(3)
nyWorstOutpatientPayments = nyWorstOutpatientMerged[['hospital_name', 'city', 'county_name', 'apc', 'average_total_payments']].sort_values(by= 'average_total_payments', ascending= False)
nyWorstOutpatientPayments.head(3)
nyWorst_outpatient = nyWorstOutpatientMerged.loc[(nyWorstOutpatientMerged['hospital_overall_rating'] == '1')]
nyWorst_outpatient
nyWorst_outpatient.groupby('hospital_name')['outpatient_services'].sum().sort_values()
nyWorst_outpatient.outpatient_services.sum()

# =============================================================================
# Comparing top hospitals within NY based on hospital ratings
# =============================================================================
hospitalNames = newyorkHospitals['hospital_name'].sort_values()
sbu = newyorkHospitals.loc[newyorkHospitals['hospital_name'] == 'SUNY/STONY BROOK UNIVERSITY HOSPITAL']
sbuCleaned = sbu.dropna(axis= 1)
nyu = newyorkHospitals.loc[newyorkHospitals['hospital_name'] == 'NEW YORK UNIVERSITY LANGONE MEDICAL CENTER']
nyuCleaned = nyu.dropna(axis= 1)
bhs = newyorkHospitals.loc[newyorkHospitals['hospital_name'] == 'BELLEVUE HOSPITAL CENTER']
bhsCleaned = bhs.dropna(axis= 1)
sbu_vs_nyu_vs_bhs = pd.concat([nyuCleaned, sbuCleaned, bhsCleaned])

mmc = newyorkHospitals.loc[newyorkHospitals['hospital_name'] == 'MAIMONIDES MEDICAL CENTER']

# =============================================================================
# Visualizations
# =============================================================================

ny_BestPayments = nyBestMerged[['hospital_name', 'average_total_payments']].groupby('hospital_name')['average_total_payments'].sum().round(2).sort_values(ascending=False).to_frame().reset_index()
ny_BestPayments.head(2)
nyc_BestPayments = nycBestMerged[['hospital_name', 'average_total_payments']].groupby('hospital_name')['average_total_payments'].sum().round(2).sort_values(ascending=False).to_frame().reset_index()
nyc_BestPayments.head(2)
ny_WorstPayments = nyWorstMerged[['hospital_name', 'average_total_payments']].groupby('hospital_name')['average_total_payments'].sum().round(2).sort_values(ascending=False).to_frame().reset_index()
ny_WorstPayments.head(2)
nyc_WorstPayments = nycWorstMerged[['hospital_name', 'average_total_payments']].groupby('hospital_name')['average_total_payments'].sum().round(2).sort_values(ascending=False).to_frame().reset_index()
nyc_WorstPayments.head(2)

plt.figure(figsize=(10,5))
fig1 = sns.barplot(x='hospital_name', y='average_total_payments', data=nyBestMerged, palette='Set2')
plt.title('New York Best Hospitals with a Rating of 4 or Higher')
fig1.set_xticklabels(fig1.get_xticklabels(), rotation=90, horizontalalignment='right')
fig1.set(xlabel='Hospital Names', ylabel='Average Total Payments Across All DRGs')
plt.show()

nyBestMerged.hospital_name.nunique()
#To verify the total number of columns; delete later

plt.figure(figsize=(10,5))
fig2 = sns.barplot(x='hospital_name', y='average_total_payments', data=nycBestMerged, palette='Set2')
plt.title('New York City Best Hospitals with a Rating of 4 or Higher')
fig2.set_xticklabels(fig2.get_xticklabels(), rotation=45, horizontalalignment='right')
fig2.set(xlabel='Hospital Names', ylabel='Average Total Payments Across All DRGs')
plt.show()

plt.figure(figsize=(10,5))
fig3 = sns.barplot(x='hospital_name', y='average_total_payments', data=ny_BestPayments, palette='Set2')
plt.title('New York Best Hospitals with a Rating of 4 or Higher')
fig3.set_xticklabels(fig3.get_xticklabels(), rotation=90, horizontalalignment='right')
fig3.set(xlabel='Hospital Names', ylabel='Sum of The Average Total Payments Across All DRGs')
plt.show()

plt.figure(figsize=(10,5))
fig4 = sns.barplot(x='hospital_name', y='average_total_payments', data=nyc_BestPayments, palette='Set2')
plt.title('New York City Best Hospitals with a Rating of 4 or Higher')
fig4.set_xticklabels(fig4.get_xticklabels(), rotation=45, horizontalalignment='right')
fig4.set(xlabel='Hospital Names', ylabel='Sum of The Average Total Payments Across All DRGs')
plt.show()

plt.figure(figsize=(20,5))
fig5 = sns.barplot(x='hospital_name', y='average_total_payments', data=nyWorstMerged, palette= 'Set3')
plt.title('New York Worst Hospitals with a Rating of 2 or Lower')
fig5.set_xticklabels(fig5.get_xticklabels(), rotation=90, horizontalalignment='right')
fig5.set(xlabel='Hospital Names', ylabel='Average Total Payments Across All DRGs')
plt.show()

plt.figure(figsize=(10,5))
fig6 = sns.barplot(x='hospital_name', y='average_total_payments', data=nycWorstMerged, palette='Set3')
plt.title('New York City Worst Hospitals with a Rating of 2 or Lower')
fig6.set_xticklabels(fig6.get_xticklabels(), rotation=90, horizontalalignment='right')
fig6.set(xlabel='Hospital Names', ylabel='Average Total Payments Across All DRGs')
plt.show()

plt.figure(figsize=(10,5))
fig7 = sns.barplot(x='hospital_name', y='average_total_payments', data=nyc_WorstPayments, palette='Set3')
plt.title('New York City Worst Hospitals with a Rating of 2 or Lower')
fig7.set_xticklabels(fig7.get_xticklabels(), rotation=90, horizontalalignment='right')
fig7.set(xlabel='Hospital Names', ylabel='Sum of The Average Total Payments Across All DRGs')
plt.show()

sbuInpatient.drg_definition.count()
sbu20Payments = sbuPayments.head(10).append(sbuPayments.tail(10))
sburandomPayments = sbuInpatient.sample(20)

plt.figure(figsize=(10,5))
fig8 = sns.barplot(x='drg_definition', y='average_total_payments', data=sbu20Payments, palette= 'Set1')
plt.title('Stony Brook University Hospital: Top 10 and Bottom 10 DRG Costs')
plt.xticks(rotation=45, horizontalalignment='right', fontsize='smaller')
fig8.set(xlabel='Diagnosis Related Groups (DRGs) within SBU Hospital', ylabel='Average Total Payments Per DRG')
plt.show()

plt.figure(figsize=(10,5))
fig9 = sns.barplot(x='drg_definition', y='average_total_payments', data=sburandomPayments, palette= 'Set1')
plt.title('Stony Brook University Hospital: Random DRG Costs')
plt.xticks(rotation=45, horizontalalignment='right', fontsize='smaller')
fig9.set(xlabel='Diagnosis Related Groups (DRGs) within SBU Hospital', ylabel='Average Total Payments Per DRG')
plt.show()

plt.figure(figsize=(10,5))
fig10 = sns.barplot(x='apc', y='average_total_payments', data=sbuOutpatientPayments, palette= 'Set1')
plt.title('Stony Brook University Hospital: APC Costs')
plt.xticks(rotation=45, horizontalalignment='right', fontsize='smaller')
fig10.set(xlabel='Ambulatory Payment Classifications within SBU Hospital', ylabel='Average Total Payments Per APC')
plt.show()
