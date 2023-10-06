import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt


def seperate_num_obj_columns(data):
    object_columns=[col for col in data.columns if data[col].dtype == np.object0]
    num_columns=[col for col in data.columns if col not in object_columns]
    return object_columns,num_columns

def plot_line(data,x=None):
    object_columns,num_columns=seperate_num_obj_columns(data)
    if x is None:
        plt.plot(np.arange(data.shape[0]),data[num_columns])
        st.pyplot(plt)
        return plt
    
def plot_scatter(data,x=None):
    object_columns,num_columns=seperate_num_obj_columns(data)
    if x is None:
        for col in num_columns:
            try:
                plt.scatter(np.arange(data.shape[0]),data[col])
            except:
                pass
        st.pyplot(plt)
        return plt