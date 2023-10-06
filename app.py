import os
from io import BytesIO
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import chart_types as ct

st.set_page_config(layout="wide")

with open("styles/style.css", "r") as css_file:
    custom_css = css_file.read()

# Render the custom CSS
st.markdown(f"<style>{custom_css}</style>", unsafe_allow_html=True)

if 'counter' not in st.session_state:
    st.session_state.counter = 0
st.session_state.counter += 1
st.write(f"Counter: {st.session_state.counter}")

if st.session_state.counter==1:
    print("removed")
    os.remove("temp_file.csv")

try:
    data = pd.read_csv("temp_file.csv")
except:
    data = pd.DataFrame({"X": [None, None, None], "Y": [None, None, None]})

def save_chart_as_image():
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    return buffer

new_columns = st.text_input("You can add columns here")
if st.button("Add columns"):
    for col in new_columns.split(","):
        if col not in data.columns:
            data[col] = None  # Only add the column if it doesn't already exist

chart_type = "line"
chart_type = st.selectbox("Select the chart type you want to create", ["line", "scatter"])
col1, col2 = st.columns(2)
with col1:
    data = st.data_editor(data, num_rows="dynamic")
    st.dataframe(data)
    data.to_csv("temp_file.csv", index=False)

with col2:
    if chart_type == "line":
        ct.plot_line(data)
    elif chart_type == "scatter":
        ct.plot_scatter(data)

    chart_buffer = save_chart_as_image()
    st.download_button(
        label="Download Chart as Image",
        data=chart_buffer,
        file_name="sample_chart.png",
        key="download_chart"
    )

# Check if running in Streamlit sharing environment
if 'SHARING_HOST' in os.environ:
    # Schedule the deletion of the temporary file when the app exits
    import atexit
    
    def delete_temp_file():
        print("done")
        if os.path.exists("temp_file.csv"):
            os.remove("temp_file.csv")
    
    atexit.register(delete_temp_file)
