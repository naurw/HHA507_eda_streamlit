#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 13 15:34:26 2021

@author: William
"""

import pandas as pd 
import glob
import os

# =============================================================================
# Loading dataframes
# =============================================================================
path = os.getcwd()
print('Current default local path is:', path)
csv_files = glob.glob(os.path.join(path, 'Desktop/AHI_DataSci_507/Deployment_Streamlit', '*.csv'))
csv_files

print('The total number of csv files that will be analyzed are:', len(csv_files))
print('The file paths/names are:', csv_files)

csvList = []

for i in csv_files: 
    df = pd.read_csv(i)
    csvList.append(df)
    
    print('Location:', i)
    print('File Name:', i.split('\\')[-1])
    print('Content')
    display(df)

df = pd.concat(csvList)
print('The initial length of rows in the concatenated df should be 239722 rows. Confirm with:', len(df))
inpatient = pd.DataFrame(csvList[0])
outpatient = pd.DataFrame(csvList[1])
hospital = pd.DataFrame(csvList[2])
print('The total number of rows within hospital:', len(hospital), '.', 
      'The total number of rows within outpatient:', len(outpatient), '.', 
      'The total number of rows within inpatient:', len(inpatient), '.')

# =============================================================================
# Initial Cleaning of Dataframes 
# =============================================================================
def clean(i):
    output1 = len(i) 
    output2 = i.head(5) 
    output3 = i.tail(5)
    output4 = i.sample(20)
    output5 = i.info()
    output6 = i.isnull().sum()
    output7 = i.nunique()
    return ({'len': output1, 'head': output2, 'tail': output3, 'samp': output4, 'info': output5, 'null': output6, 'uniq': output7})

df_sample = clean(df)['samp']
inpatient_sample = clean(inpatient)['samp']
outpatient_sample = clean(outpatient)['samp']
hospital_sample = clean(hospital)['samp']

clean(outpatient)['info']
outpatient['provider_id'] = outpatient['provider_id'].astype(str)
outpatient['provider_id'].dtype
clean(outpatient)['null']

clean(inpatient)['info']
inpatient['provider_id'] = inpatient['provider_id'].astype(str)
inpatient['provider_id'].dtype
clean(inpatient)['null']

clean(hospital)['info']
clean(hospital)['null']
hospital.hospital_name.nunique()
hospital.hospital_name.value_counts().sum()
print('Within the dataframe hospital, there are a total of', hospital.hospital_name.nunique(), 'unique hospitals out of', len(hospital.hospital_name))
print('Some of the repeating hospital names are:', hospital.hospital_name.value_counts().head(20))
print('Hospitals with repeating names such as Memorial Hospital:', len(hospital[hospital['hospital_name'] == 'MEMORIAL HOSPITAL']), 'have several branches across several regions')

hospital.hospital_ownership.value_counts().sort_values()
hospitalGovt = ['Government - Federal', 'Government - State', 'Government - Local', 'Government - Hospital District or Authority', 'Department of Defense']
hospitalVol = ['Voluntary non-profit - Private', 'Voluntary non-profit - Other', 'Voluntary non-profit - Church']
hospitalInd = ['Tribal', 'Physician', 'Proprietary']
hospital.loc[hospital['hospital_ownership'].isin(hospitalGovt), 'hospital_ownership'] = 'Government'
hospital.loc[hospital['hospital_ownership'].isin(hospitalVol), 'hospital_ownership'] = 'Voluntary'
hospital.loc[hospital['hospital_ownership'].isin(hospitalInd), 'hospital_ownership'] = 'Independent'
hospital['hospital_ownership'].value_counts()
'''
Voluntary hospitals, which are all hospitals contained within hospitalVol, are the most common type of ownership: 
    
Voluntary      2956
Government     1245
Independent    1113
'''
hospital.hospital_type.value_counts()
'''
Acute care hospitals are the most common hospital type: 

Acute Care Hospitals                  3256
Critical Access Hospitals             1355
Psychiatric                            573
Childrens                               95
Acute Care - Department of Defense      35
'''

# =============================================================================
# New York State with select counties of interest 
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
inpatientMergedSample = inpatientMerged.sample(100)
cleanMerge = inpatientMerged[inpatientMerged['hospital_name'].notna()]

sbuInpatient = cleanMerge.loc[cleanMerge['hospital_name'] == 'SUNY/STONY BROOK UNIVERSITY HOSPITAL']
clean(sbuInpatient)['info']
sbuInpatientCleaned = sbuInpatient[['provider_id', 'drg_definition', 'total_discharges', 'average_covered_charges', 'average_total_payments', 'average_medicare_payments']]
charges = pd.DataFrame(sbuInpatientCleaned.groupby('drg_definition')['average_covered_charges'])
sbuCharges = sbuInpatient[['drg_definition', 'average_covered_charges']].sort_values(by='average_covered_charges', ascending=False)
sbuPayments = sbuInpatient[['drg_definition', 'average_total_payments']].sort_values(by='average_total_payments', ascending= False)
sbuMedicare = sbuInpatient[['drg_definition', 'average_medicare_payments']].sort_values(by= 'average_medicare_payments', ascending= False)
sbuDischarges = sbuInpatient[['drg_definition', 'total_discharges']].sort_values(by= 'total_discharges', ascending= False)
print('The sum of average total covered charges within SBU hospital is $', sbuInpatient.average_covered_charges.sum())
print('The sum of total inpatient discharges within SBU hospital is', sbuInpatient.total_discharges.sum())
print('The sum of average total payments within SBU hospital is $', sbuInpatient.average_total_payments.sum())
print('The sum of average medicare payments within SBU hospital is $', sbuInpatient.average_medicare_payments.sum())

clean(sbuCharges)['head']
'''
These are the top 5 most EXPENSIVE drgs (diagnosis related groups) and their average covered charges for inpatient visits within Stony Brook Hospital:
    - Most expensive: ECMO OR TRACH W MV >96 HRS OR PDX EXC FACE, MOUTH & NECK W MAJ O.R. have average charges of $763,781.83 

                                           drg_definition  average_covered_charges
200462  003 - ECMO OR TRACH W MV >96 HRS OR PDX EXC FA...                763781.83
200463  004 - TRACH W MV 96+ HRS OR PDX EXC FACE, MOUT...                493547.74
200542  266 - ENDOVASCULAR CARDIAC VALVE REPLACEMENT W...                297508.00
200658  834 - ACUTE LEUKEMIA W/O MAJOR O.R. PROCEDURE ...                294966.73
200464  023 - CRANIO W MAJOR DEV IMPL/ACUTE COMPLEX CN...                280725.53
'''
clean(sbuCharges)['tail']
'''
These are the top 5 most INEXPENSIVE drgs (diagnosis related groups) and their average covered charges for inpatient visits within Stony Brook Hospital: 
    - Note that because the sort by function had ascending= False, the most inexpensive is the LAST entry
    - Most inexpensive: RENAL FAILURE W/O CC/MCC have average charges of $17,885.91
    
                                               drg_definition  average_covered_charges
200559  310 - CARDIAC ARRHYTHMIA & CONDUCTION DISORDER...                 22473.87
200564  316 - OTHER CIRCULATORY SYSTEM DIAGNOSES W/O C...                 22092.80
200561  313 - CHEST PAIN                                                  20174.49
200588  395 - OTHER DIGESTIVE SYSTEM DIAGNOSES W/O CC/MCC                 18167.00
200645  684 - RENAL FAILURE W/O CC/MCC                                    17885.91
'''
clean(sbuPayments)['head']
'''
These are the top 5 most EXPENSIVE drgs (diagnosis related groups) and their average total payments for inpatient visits within Stony Brook Hospital:
    - Most expensive: ECMO OR TRACH W MV >96 HRS OR PDX EXC FACE, MOUTH & NECK W MAJ O.R. have average total payments of $216,636.88
    
                                           drg_definition  average_total_payments
200462  003 - ECMO OR TRACH W MV >96 HRS OR PDX EXC FA...               216636.88
200463  004 - TRACH W MV 96+ HRS OR PDX EXC FACE, MOUT...               132951.87
200658  834 - ACUTE LEUKEMIA W/O MAJOR O.R. PROCEDURE ...                93531.45
200517  216 - CARDIAC VALVE & OTH MAJ CARDIOTHORACIC P...                92679.84
200542  266 - ENDOVASCULAR CARDIAC VALVE REPLACEMENT W...                88382.63
'''
clean(sbuPayments)['tail']
'''
These are the top 5 most INEXPENSIVE drgs (diagnosis related groups) and their average covered charges for inpatient visits within Stony Brook Hospital: 
    - Note that because the sort by function had ascending= False, the most inexpensive is the LAST entry
    - Most inexpensive: CARDIAC ARRHYTHMIA & CONDUCTION DISORDERS W/O CC/MCC have average total payments of $6,796.27
    
                                           drg_definition  average_total_payments
200632  639 - DIABETES W/O CC/MCC                                         7241.82
200564  316 - OTHER CIRCULATORY SYSTEM DIAGNOSES W/O C...                 7095.20
200561  313 - CHEST PAIN                                                  7086.60
200645  684 - RENAL FAILURE W/O CC/MCC                                    6914.36
200559  310 - CARDIAC ARRHYTHMIA & CONDUCTION DISORDER...                 6796.27
'''
clean(sbuMedicare)['head']
'''
These are the top 5 most EXPENSIVE drgs (diagnosis related groups) and their average medicare payments for inpatient visits within Stony Brook Hospital:
    - Most expensive: ECMO OR TRACH W MV >96 HRS OR PDX EXC FACE, MOUTH & NECK W MAJ O.R. have average total payments of $172,514.88
    
                                           drg_definition  average_medicare_payments
200462  003 - ECMO OR TRACH W MV >96 HRS OR PDX EXC FA...                  172514.88
200463  004 - TRACH W MV 96+ HRS OR PDX EXC FACE, MOUT...                  108173.04
200542  266 - ENDOVASCULAR CARDIAC VALVE REPLACEMENT W...                   83533.44
200517  216 - CARDIAC VALVE & OTH MAJ CARDIOTHORACIC P...                   77210.62
200519  219 - CARDIAC VALVE & OTH MAJ CARDIOTHORACIC P...                   70139.57
'''
clean(sbuMedicare)['tail']
'''
These are the top 5 most INEXPENSIVE drgs (diagnosis related groups) and their average medicare payments for inpatient visits within Stony Brook Hospital: 
    - Note that because the sort by function had ascending= False, the most inexpensive is the LAST entry
    - Most inexpensive: RENAL FAILURE W/O CC/MCC have average charges of $4,010.00   
    
                                           drg_definition  average_medicare_payments
200555  303 - ATHEROSCLEROSIS W/O MCC                                        5046.55
200583  390 - G.I. OBSTRUCTION W/O CC/MCC                                    4989.54
200559  310 - CARDIAC ARRHYTHMIA & CONDUCTION DISORDER...                    4718.87
200595  440 - DISORDERS OF PANCREAS EXCEPT MALIGNANCY ...                    4299.00
200645  684 - RENAL FAILURE W/O CC/MCC                                       4010.00   
'''
clean(sbuDischarges)['head']
'''
These are the top 5 drgs most COMMON (diagnosis related groups) and their discharge numbers for inpatient visits within Stony Brook Hospital: 
    - Most common: SEPTICEMIA OR SEVERE SEPSIS W/O MV 96+ HOURS W MCC have 628 total discharges 

                                           drg_definition  total_discharges
200668  871 - SEPTICEMIA OR SEVERE SEPSIS W/O MV 96+ H...               628
200602  470 - MAJOR JOINT REPLACEMENT OR REATTACHMENT ...               286
200549  287 - CIRCULATORY DISORDERS EXCEPT AMI, W CARD...               221
200533  247 - PERC CARDIOVASC PROC W DRUG-ELUTING STEN...               220
200550  291 - HEART FAILURE & SHOCK W MCC                               195
'''
clean(sbuDischarges)['tail']
'''
These are the top 5 drgs most UNCOMMON (diagnosis related groups) and their discharge numbers for inpatient visits within Stony Brook Hospital:
    
                                          drg_definition  total_discharges
200483  083 - TRAUMATIC STUPOR & COMA, COMA >1 HR W CC                  11
200616  545 - CONNECTIVE TISSUE DISORDERS W MCC                         11
200635  644 - ENDOCRINE DISORDERS W CC                                  11
200632  639 - DIABETES W/O CC/MCC                                       11
200622  580 - OTHER SKIN, SUBCUT TISS & BREAST PROC W CC                11
'''
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
charges2 = pd.DataFrame(sbuOutpatientCleaned.groupby('apc')['average_estimated_submitted_charges'])
sbuOutpatientCharges = sbuOutpatient[['apc', 'average_estimated_submitted_charges']].sort_values(by='average_estimated_submitted_charges', ascending=False)
sbuOutpatientPayments = sbuOutpatient[['apc', 'average_total_payments']].sort_values(by='average_total_payments', ascending=False)
sbuOutpatientServices = sbuOutpatient[['apc', 'outpatient_services']].sort_values(by='outpatient_services', ascending=False)
print('The sum of all outpatient services within SBU hospital is', sbuOutpatient.outpatient_services.sum())
print('The sum of average estimated submitted charges is $', sbuOutpatient.average_estimated_submitted_charges.sum().round(2))
print('The sum of average total payments is $', sbuOutpatient.average_total_payments.sum().round(2))

sbuOutpatientCharges.head(5).round(2)
'''
These are the top 5 most EXPENSIVE apc (ambulatory related groups) and their average estimated submitted charges for inpatient visits within Stony Brook Hospital:
    - Most expensive: Level IV Endoscopy Upper Airway have average estimated submitted charges of $8,645.62

                                                   apc  average_estimated_submitted_charges
32322           0074 - Level IV Endoscopy Upper Airway                              8645.62
32331                  0377 - Level II Cardiac Imaging                              6586.44
32321                 0020 - Level II Excision/ Biopsy                              4639.93
32329  0270 - Level II Echocardiogram Without Contrast                              4050.39
32328   0269 - Level I Echocardiogram Without Contrast                              3025.16
'''
sbuOutpatientPayments.head(5).round(2)
'''
These are the top 5 most EXPENSIVE apc (ambulatory related groups) and their average total payments for inpatient visits within Stony Brook Hospital:
    - Most expensive: Level IV Endoscopy Upper Airway have average total payments of $2,307.21
    
                                          apc  average_total_payments
32322  0074 - Level IV Endoscopy Upper Airway                 2307.21
32323        0203 - Level IV Nerve Injections                 1325.64
32331         0377 - Level II Cardiac Imaging                 1300.67
32321        0020 - Level II Excision/ Biopsy                  948.68
32325       0207 - Level III Nerve Injections                  697.66
'''
sbuOutpatientServices.head(5).round(2)
'''
These are the top 5 most COMMON apc (ambulatory related groups) and their average medicare payments for inpatient visits within Stony Brook Hospital:
    - Most common: Level I Echocardiogram Without Contrast have average outpatient services of 1,119

                                                     apc  outpatient_services
32328     0269 - Level I Echocardiogram Without Contrast                 1119
32326  0265 - Level I Diagnostic and Screening Ultras...                  765
32332                      0634 - Hospital Clinic Visits                  626
32331                    0377 - Level II Cardiac Imaging                  519
32327  0267 - Level III Diagnostic and Screening Ultr...                  494
'''
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
    - BUT YOU CAN WORK AROUND by changing the list of integers into a list of strings to filter out what we want/don't want 
'''

def ratingsFilter (i): 
    outRatings = i.isin(ratings)
    outHigh = i.isin(high)
    outLow = i.isin(low)
    outMid = i.isin(mid)
    return ({'Ratings': outRatings, 'High': outHigh, 'Low': outLow, 'Mid': outMid})

nyRatings = newyorkHospitals[ratingsFilter(newyorkHospitals.hospital_overall_rating)['Ratings']]
nyRatingsHospital = nyRatings[['hospital_overall_rating', 'hospital_name']]
nyRatings.groupby('hospital_name')['hospital_overall_rating'].count()
nyBest = newyorkHospitals[ratingsFilter(newyorkHospitals.hospital_overall_rating)['High']]
clean(nyBest)['null']

def cleaned (i):
    outAll = i.loc[:, ~i.columns.isin(['hospital_overall_rating_footnote', 'mortality_national_comparison_footnote', 'safety_of_care_national_comparison_footnote', 
                                    'readmission_national_comparison_footnote', 'patient_experience_national_comparison_footnote', 'effectiveness_of_care_national_comparison_footnote', 
                                    'timeliness_of_care_national_comparison_footnote', 'efficient_use_of_medical_imaging_national_comparison_footnote', 'location'])]
    outKeep = i.loc[:, ~i.columns.isin(['hospital_overall_rating_footnote', 'mortality_national_comparison_footnote', 'safety_of_care_national_comparison_footnote', 
                                    'readmission_national_comparison_footnote', 'patient_experience_national_comparison_footnote', 'effectiveness_of_care_national_comparison_footnote', 
                                    'timeliness_of_care_national_comparison_footnote', 'efficient_use_of_medical_imaging_national_comparison_footnote'])]
    five = i.loc[(i['hospital_overall_rating'] == '5')]
    one = i.loc[(i['hospital_overall_rating'] == '1')]
    compare = i[['provider_id', 'hospital_name', 'mortality_national_comparison', 'safety_of_care_national_comparison', 'readmission_national_comparison', 
                                    'patient_experience_national_comparison', 'effectiveness_of_care_national_comparison', 'timeliness_of_care_national_comparison', 
                                    'efficient_use_of_medical_imaging_national_comparison']]
    return ({'none': outAll, 'keep': outKeep, '5': five, '1': one, 'comp': compare})

nyBestCleaned = cleaned(nyBest)['none']
print('There are more hospitals (18) within New York State with a rating of 4 as seen below:', nyBestCleaned['hospital_overall_rating'].value_counts())
print('There are more acute care hospitals (19) within New York State with a rating of 4 or higher as seen below:', nyBestCleaned['hospital_type'].value_counts())
print('There are more voluntary or nonprofit (20) hospitals within New York State with a rating of 4 or higher as seen below:', nyBestCleaned['hospital_ownership'].value_counts())
nyBestCleaned['county_name'].value_counts().head(3)
'''
The number of hospitals within New York State with the HIGHEST overall ratings (4-5): 
    - New York City has the most hospitals within its 5 boroughs in New York State
    - New York (Manhattan) has 4 of New York's highly rated hospitals
    
NEW YORK        4
ST. LAWRENCE    3
SUFFOLK         2
'''
nyBestCleaned['mortality_national_comparison'].value_counts()
'''
Same as the national average    11
Above the national average       8
Not Available                    2
'''
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
'''
The number of hospitals within New York State with the LOWEST overall ratings (4-5): 
    - New York City has the most hospitals within its 5 boroughs in New York State
    - Kings leading the worst hospitals with Bronx and Queens tied 

KINGS     10
BRONX      6
QUEENS     6
'''
len(nyWorstCleaned)
nyWorst46 = cleaned(nyWorstCleaned)['1']
nycWorst23 = nyWorstCleaned.loc[(nyWorstCleaned['hospital_overall_rating'] == '1') & (nyWorstCleaned['county_name'].isin(nycCounty))]
nycWorst23Comparison = cleaned(nycWorst23)['comp']
nycWorst23.effectiveness_of_care_national_comparison.value_counts()
'''
Same as the national average    13
Below the national average      10
'''
nycBelowEffectiveness = nycWorst23[nycWorst23['effectiveness_of_care_national_comparison'] == 'Below the national average']
nycBelowEffectiveness[['hospital_name']]
'''
These are the poorest performers within NYC (lowest ratings and below effectiveness of care)

4    LINCOLN MEDICAL & MENTAL HEALTH CENTER
20                   QUEENS HOSPITAL CENTER
29       RICHMOND UNIVERSITY MEDICAL CENTER
75        BROOKDALE HOSPITAL MEDICAL CENTER
80          JAMAICA HOSPITAL MEDICAL CENTER
94      NYC HEALTH + HOSPITALS/CONEY ISLAND
103                   JACOBI MEDICAL CENTER
152                    ST BARNABAS HOSPITAL
170                ELMHURST HOSPITAL CENTER
182            KINGS COUNTY HOSPITAL CENTER
'''

# =============================================================================
# New York State and New York City Hospitals based on inpatient data  
# =============================================================================
nyBestMerged = inpatient.merge(nyBestCleaned, how='left', on='provider_id')
nyBestMerged = nyBestMerged[nyBestMerged['hospital_name'].notna()]
nyDischarges = nyBestMerged[['hospital_name', 'city', 'county_name', 'drg_definition', 'total_discharges']].sort_values(by= 'total_discharges', ascending= False)
nyDischarges.head(3) 
'''
Top discharges based on hospitals + respective drgs

                                     hospital_name  ... total_discharges
112977                HOSPITAL FOR SPECIAL SURGERY  ...             3990
112597  NEW YORK UNIVERSITY LANGONE MEDICAL CENTER  ...              942
180539                GARNET HEALTH MEDICAL CENTER  ...              751
'''
nyCharges = nyBestMerged[['hospital_name', 'city', 'county_name', 'drg_definition', 'average_covered_charges']].sort_values(by= 'average_covered_charges', ascending= False)
nyCharges.head(3)
'''
Top covered charges based on hospitals + respective drgs

                                     hospital_name  ... average_covered_charges
199153      ST FRANCIS HOSPITAL - THE HEART CENTER  ...               849902.69
200462        SUNY/STONY BROOK UNIVERSITY HOSPITAL  ...               763781.83
112466  NEW YORK UNIVERSITY LANGONE MEDICAL CENTER  ...               705897.00
'''
nyPayments = nyBestMerged[['hospital_name', 'city', 'county_name', 'drg_definition', 'average_total_payments']].sort_values(by= 'average_total_payments', ascending= False)
nyPayments.head(3)
'''
Top total payments based on hospitals + respective drgs
- Mount Sinai appears twice due to different DRGs; view dataframe to see more

                               hospital_name  ... average_total_payments
110631                  MOUNT SINAI HOSPITAL  ...              275677.10
110632                  MOUNT SINAI HOSPITAL  ...              219016.63
200462  SUNY/STONY BROOK UNIVERSITY HOSPITAL  ...              216636.88
'''
nyMedicare = nyBestMerged[['hospital_name', 'city', 'county_name', 'drg_definition', 'average_medicare_payments']].sort_values(by= 'average_medicare_payments', ascending= False)
nyMedicare.head(3)
'''
Top medicare payments based on hospitals + respective drgs

                                     hospital_name  ... average_medicare_payments
110631                        MOUNT SINAI HOSPITAL  ...                 240922.20
112466  NEW YORK UNIVERSITY LANGONE MEDICAL CENTER  ...                 184864.40
200462        SUNY/STONY BROOK UNIVERSITY HOSPITAL  ...                 172514.88
'''
nyBestMerged.total_discharges.sum()
'''75885'''
nyBest3_inpatient = nyBestMerged.loc[(nyBestMerged['hospital_overall_rating'] == '5')]
nyBest3_inpatient.groupby('hospital_name')['total_discharges'].sum().sort_values()
'''
HOSPITAL FOR SPECIAL SURGERY                  6211
ST FRANCIS HOSPITAL - THE HEART CENTER        7447
NEW YORK UNIVERSITY LANGONE MEDICAL CENTER    8527
'''
nyBest3_inpatient.groupby('hospital_name')['average_total_payments'].sum().sort_values()
'''
HOSPITAL FOR SPECIAL SURGERY                   811799.99
ST FRANCIS HOSPITAL - THE HEART CENTER        3021074.89
NEW YORK UNIVERSITY LANGONE MEDICAL CENTER    5652937.56
'''
nyBest3_inpatient.groupby('hospital_name')['average_medicare_payments'].sum().sort_values()
'''
HOSPITAL FOR SPECIAL SURGERY                   636277.83
ST FRANCIS HOSPITAL - THE HEART CENTER        2694288.45
NEW YORK UNIVERSITY LANGONE MEDICAL CENTER    4679072.03
'''
nyBest3_inpatient.groupby('hospital_name')['average_covered_charges'].sum()
'''
HOSPITAL FOR SPECIAL SURGERY                   2732782.68
NEW YORK UNIVERSITY LANGONE MEDICAL CENTER    25286694.79
ST FRANCIS HOSPITAL - THE HEART CENTER        17064058.00
'''
nyBest3_inpatient.total_discharges.sum()
'''22185'''
                    
nycBestMerged = nyBestMerged[nyBestMerged['county_name'].isin(nycCounty)]
nycBestMerged.info()
nycDischarges = nycBestMerged[['hospital_name', 'drg_definition', 'total_discharges']].sort_values(by= 'total_discharges', ascending= False)
nycDischarges.head(3) 
'''
112977                HOSPITAL FOR SPECIAL SURGERY  ...             3990
112597  NEW YORK UNIVERSITY LANGONE MEDICAL CENTER  ...              942
110891                        MOUNT SINAI HOSPITAL  ...              560
'''
nycCharges = nycBestMerged[['hospital_name', 'drg_definition', 'average_covered_charges']].sort_values(by= 'average_covered_charges', ascending= False)
nycCharges.head(3)
'''
112466  NEW YORK UNIVERSITY LANGONE MEDICAL CENTER  ...               705897.00
112588  NEW YORK UNIVERSITY LANGONE MEDICAL CENTER  ...               621089.67
110631                        MOUNT SINAI HOSPITAL  ...               588095.50
'''
nycPayments = nycBestMerged[['hospital_name', 'drg_definition', 'average_total_payments']].sort_values(by= 'average_total_payments', ascending= False)
nycPayments.head(3)
'''
110631                        MOUNT SINAI HOSPITAL  ...              275677.10
110632                        MOUNT SINAI HOSPITAL  ...              219016.63
112466  NEW YORK UNIVERSITY LANGONE MEDICAL CENTER  ...              192587.60
'''
nycMedicare = nycBestMerged[['hospital_name', 'drg_definition', 'average_medicare_payments']].sort_values(by= 'average_medicare_payments', ascending= False)
nycMedicare.head(3)
'''
110631                        MOUNT SINAI HOSPITAL  ...                 240922.20
112466  NEW YORK UNIVERSITY LANGONE MEDICAL CENTER  ...                 184864.40
110632                        MOUNT SINAI HOSPITAL  ...                 157560.68
'''
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

# =============================================================================
# Visualizations
# =============================================================================
import matplotlib.pyplot as plt
import seaborn as sns

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

# =============================================================================
# for tesitng purposes: 
# nytest = nyBestMerged[[col for col in nyBestMerged.columns if 'ECMO OR TRACH' in col]]
# nyBestMerged['hospital_name'] = nyBestMerged['hospital_name'].astype(str)
# nyBestMerged.hospital_name.dtypes
# fnytest = nyBestMerged.filter(like='STONY BROOK', axis=1)
# sbuecmo1 = sbuInpatient[[col for col in sbuInpatient.columns if 'ECMO OR TRACH' in col]]
# sbuecmo = sbuInpatient['drg_definition'].filter(like='ECMO OR TRACH')
# 
# =============================================================================
