import streamlit as st

import pandas as pd

# Set the title of the app
st.set_page_config(layout='wide')

col1, col2 = st.columns([3, 3])

@st.experimental_fragment
def upload_1():
    uploaded_file_1 = st.file_uploader("Choose a file", type=["csv"], key='file_1')

    if uploaded_file_1:
        if uploaded_file_1.type is not None:
        
            df_1 = pd.read_csv(uploaded_file_1, index_col=0)

            st.write(df_1.head())

            return df_1

@st.experimental_fragment
def upload_2():
    uploaded_file_2 = st.file_uploader("Choose a file", type=["xlsx"], key='file2')

    if uploaded_file_2:
        if uploaded_file_2.type is not None:
    
            df_2 = pd.read_excel(uploaded_file_2, engine='openpyxl', sheet_name=0)

            st.write(df_2.head())

            return df_2
with col1:
    st.title("上传销售退货数据")
    net_sales_df = upload_1()
    
    
    # Create a file uploader widget


with col2:
    st.title("上传重量数据")
    weight_df = upload_2()

@st.cache_data
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv(sep=";").encode("utf-8-sig")

# Add a button to process the uploaded file
# merged_df = None
st.session_state['data'] = False
if st.button("合并", type="primary"):
    all_weight_df = net_sales_df.merge(weight_df, left_on="No_", right_on="No.", how="left")
    all_weight_df['total_weight'] = all_weight_df['产品净重'] * all_weight_df['net sales']
    file_out = convert_df(all_weight_df)
    st.session_state['data'] = True

if st.session_state.get('data', None) == True:
    st.download_button(
    label="下载为 CSV",
    data=file_out,
    file_name="output.csv",
    mime="text/csv",
)





