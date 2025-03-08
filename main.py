import streamlit as st
import pandas as pd
from io import BytesIO
from utils import read_csv
from data_prepocessing import remove_duplicates, clean_text_column, regex_options, setup_custom_stopwords, remove_stopwords

# Title of the program
st.title("Data Cleaner for NLP")
menu = ["Data Cleaner"]
choices = st.sidebar.selectbox("Menu", menu)

if choices == "Data Cleaner":
    st.subheader("Data Cleaning")
    uploaded_file = st.file_uploader("Upload The CSV/Excel File")

    #Remove Duplicates
    clean_duplicate = st.sidebar.checkbox("Remove Duplicate")

    #Remove Special Characters
    clean_special_char = st.sidebar.checkbox("Remove Special Character")


    #Remove Stopwords
    clean_stopwords = st.sidebar.checkbox("Remove Stopwords")


    if uploaded_file is not None:
        
        raw_df = read_csv(uploaded_file)
        column_to_clean = st.selectbox("Choose Column to be Cleaned", raw_df.columns)
        selected_regex = st.multiselect("Choose Regex for Data Cleaning ", options=list(regex_options.keys()))
        stopwords_input = st.text_area("Insert More Stopwords if Necessary (separate with comma): ", help="Example : word1, word2, word satu, word dua")
        col1, col2 = st.columns(2)

        with col1 :
             with st.expander("Original Dataframe"):
                  st.write("### Dataframe ###")
                  st.write(raw_df)
                  st.write("Total Rows : ",len(raw_df))

        with col2 :
             clean_df = raw_df
             with st.expander("Cleaned Dataframe"):
                  if clean_duplicate:
                       clean_df = remove_duplicates(clean_df, column_to_clean)
                  if clean_special_char:
                       clean_df = clean_text_column(clean_df, column_to_clean, selected_regex)
                  if clean_stopwords:
                       custom_stopwords = setup_custom_stopwords(stopwords_input)
                       clean_df[column_to_clean] = clean_df[column_to_clean].apply(lambda x: remove_stopwords(x, custom_stopwords))
                
                  st.write(clean_df)
                  st.write("Total Rows : ",len(clean_df))

df = clean_df
#Option to download processed data
st.write("### Download The Result")
name = st.text_input("Input the name of downloaded file (ends with '.csv' or '.xlsx') :", help=("Example : df.csv or df.xlsx"))
csv = df.to_csv(index=False).encode("utf-8")
st.download_button(
     label="Download CSV",
     data=csv,
     file_name=name,
     mime="text/csv"
)

excel_buffer = BytesIO()
with pd.ExcelWriter(excel_buffer, engine="openpyxl") as writer:
     df.to_excel(writer, index=False, sheet_name="Cleaned Dataframe")

excel_buffer.seek(0)

st.download_button(
     label="Download_Excel",
     data=excel_buffer,
     file_name=name,
     mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
)