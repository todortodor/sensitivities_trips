#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 18 17:45:42 2023

@author: slepot
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st
import time
sns.set_theme('talk')
start = time.perf_counter()

# @st.cache_data
def load_data():
    df = pd.read_csv('all_sensitivity_table_20.csv',index_col=0)
    df = df.drop(['RD_'+c for c in ['CHN','IND','BRA','RUS','ROW','MEX']])
    df = df.drop(['RP_USA'])
    df2 = pd.read_csv('all_sensitivity_table_20_1020.csv',index_col=0)
    df2 = df2.drop(['RD_'+c for c in ['CHN','IND','BRA','RUS','ROW','MEX']])
    df2 = df2.drop(['RP_USA'])
    return df, df2

dfs = load_data()
df = dfs[0]
df2 = dfs[1]

moments = ['kappa','sigma','rho','TO','TE','KM','UUPCOST','OUT','GROWTH','GPDIFF',   'SINNOVPATUS',   
       'DOMPATINUS',  'SRGDP', 'RD', 'RP','SPFLOW']
parameters = ['k', 'g_0', 'fe', 'fo', 'zeta', 'nu', 'theta', 'delta', 'eta', 
              'T']

container = st.sidebar.container()
all_moments = st.sidebar.checkbox("Add or remove all moments",True) 

if all_moments:
    selected_moments = container.multiselect("Select one or more options:",
         moments,moments)
else:
    selected_moments =  container.multiselect("Select one or more options:",
        moments)

container2 = st.sidebar.container()
all_parameters = st.sidebar.checkbox("Add or remove all parameters",True)
 
if all_parameters:
    selected_parameters = container2.multiselect("Select one or more options:",
         parameters,parameters)
else:
    selected_parameters =  container2.multiselect("Select one or more options:",
        parameters)

st.write('Choose subsets of moments / parameters on the left')
st.write('Saturate colors means the colormap range is computed with robust quantiles instead of extreme values')
st.write('Normalize rows / cols means that the (absolute) max along each row / col will be 1. Both cant be on at the same time, row has priority.')

left, center, right = st.columns(3)

with left:
    saturate = st.checkbox("Saturate colors",False) 
with center:
    normalize_columns = st.checkbox("Normalize rows (priority)",False) 
with right:
    normalize_rows = st.checkbox("Normalize cols",False) 

countries = ['USA', 'EUR', 'JAP', 'CHN', 'BRA', 'IND', 'CAN',
                  'KOR', 'RUS', 'MEX', 'ROW']

if len(selected_parameters) == 0 or len(selected_moments) == 0:
    st.write('Choose moments & parameters on the left')
    st.stop()

def replace_item(the_list):
    for item in the_list:
        if item in ['SRGDP', 'RP']:
            for c in countries:
                if c != 'USA':
                    yield item+'_'+c
        elif item in ['delta', 'eta']:
            for c in countries:
                yield item+' '+c
        elif item in ['RD']:
            for c in ['USA','EUR','JAP','CAN','KOR']:
                yield item+'_'+c
        elif item in ['T']:
            for c in countries:
                yield 'T Patent '+c
            for c in countries:
                yield 'T Non patent '+c
        elif item in ['SPFLOW']:
            for c in countries:
                yield 'SPFLOW_origin_'+c
            for c in countries:
                yield 'SPFLOW_destination_'+c
        else:
            yield item

df = df.loc[list(replace_item(selected_moments))][list(replace_item(selected_parameters))]

if normalize_columns:
    df = (df.T/df.T.abs().max()).T
if normalize_rows:
    df = df/df.abs().max()

container3 = st.container()

fig,ax = plt.subplots(figsize=(24,20),dpi=144)

sns.heatmap(df,ax=ax,
            cmap="vlag",
            center=0,
            robust = saturate,
            # square = True
            )
ax.tick_params('x', top=True, labeltop=True,labelrotation=90)


left, right = st.columns(2)

with left:
    fn = str(selected_moments)+str(selected_parameters
                          )+str(saturate
                          )+str(normalize_columns
                          )+str(normalize_rows)+'.png'
    plt.savefig(fn)
    with open(fn, "rb") as img:
        btn = st.download_button(
            label="Download image",
            data=img,
            file_name=fn,
            mime="image/png"
        )

def convert_df_to_csv(df):
  # IMPORTANT: Cache the conversion to prevent computation on every rerun
  return df.to_csv().encode('utf-8')

with right:
    st.download_button(
      label="Download data",
      data=convert_df_to_csv(df),
      file_name=str(selected_moments)+str(selected_parameters
                            )+str(saturate
                            )+str(normalize_columns
                            )+str(normalize_rows)+'.csv',
      mime='text/csv',
    )
                
container3.pyplot(fig)

selected_moments_2 = [s for s in selected_moments if s not in ['kappa', 'sigma', 'rho']]

df2 = df2.loc[list(replace_item(selected_moments_2))][list(replace_item(selected_parameters))]

if normalize_columns:
    df2 = (df2.T/df2.T.abs().max()).T
if normalize_rows:
    df2 = df2/df2.abs().max()

container4 = st.container()

fig,ax = plt.subplots(figsize=(24,20),dpi=144)

sns.heatmap(df2,ax=ax,
            cmap="vlag",
            center=0,
            robust = saturate,
            # square = True
            )
ax.tick_params('x', top=True, labeltop=True,labelrotation=90)


# left, right = st.columns(2)

# with left:
#     fn = str(selected_moments)+str(selected_parameters
#                           )+str(saturate
#                           )+str(normalize_columns
#                           )+str(normalize_rows)+'.png'
#     plt.savefig(fn)
#     with open(fn, "rb") as img:
#         btn = st.download_button(
#             label="Download image",
#             data=img,
#             file_name=fn,
#             mime="image/png"
#         )

# def convert_df2_to_csv(df2):
#   # IMPORTANT: Cache the conversion to prevent computation on every rerun
#   return df2.to_csv().encode('utf-8')

# with right:
#     st.download_button(
#       label="Download data",
#       data=convert_df2_to_csv(df2),
#       file_name=str(selected_moments)+str(selected_parameters
#                             )+str(saturate
#                             )+str(normalize_columns
#                             )+str(normalize_rows)+'.csv',
#       mime='text/csv',
#     )
                
container4.pyplot(fig)

                                  
st.write(time.perf_counter()-start)