import streamlit as st
import pandas as pd
import io
import base64
from streamlit_option_menu import option_menu
from PIL import Image


st.set_page_config(page_title="Data Cleaning Tool")

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
selected = option_menu(
    menu_title=None,
    options=["Detection","About"],
    icons=["search","book"],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal",
)
if selected == "Clean data":

    st.title("CLEANSWEEP")

    st.markdown("Upload one or multiple CSV files to preprocess and clean your files quickly and stress free.")

    uploaded_files = st.file_uploader("Choose CSV files", type="csv", accept_multiple_files=True)

    dataframes = []

    if uploaded_files:
        for file in uploaded_files:
            file.seek(0)
            df = pd.read_csv(file,encoding='Latin-1')
            # s3 = pd.read_csv(working_dir+"S3.csv", sep=",", encoding='Latin-1')
            dataframes.append(df)

        if len(dataframes) > 1:
            merge = st.checkbox("Merge uploaded CSV files")

            if merge:
                # Merge options
                keep_first_header_only = st.selectbox("Keep only the header (first row) of the first file", ["Yes", "No"])
                remove_duplicate_rows = st.selectbox("Remove duplicate rows", ["No", "Yes"])
                remove_empty_rows = st.selectbox("Remove empty rows", ["Yes", "No"])
                end_line = st.selectbox("End line", ["\\n", "\\r\\n"])

                try:
                    if keep_first_header_only == "Yes":
                        for i, df in enumerate(dataframes[1:]):
                            df.columns = dataframes[0].columns.intersection(df.columns)
                            dataframes[i+1] = df

                    merged_df = pd.concat(dataframes, ignore_index=True, join='outer')

                    if remove_duplicate_rows == "Yes":
                        merged_df.drop_duplicates(inplace=True)

                    if remove_empty_rows == "Yes":
                        merged_df.dropna(how="all", inplace=True)

                    dataframes = [merged_df]

                except ValueError as e:
                    st.error("Please make sure columns match in all files. If you don't want them to match, select 'No' in the first option.")
                    st.stop()

        # Show or hide DataFrames
        show_dataframes = st.checkbox("Show DataFrames", value=True)

        if show_dataframes:
            for i, df in enumerate(dataframes):
                st.write(f"DataFrame {i + 1}")
                st.dataframe(df)

        if st.button("Download cleaned data"):
            for i, df in enumerate(dataframes):
                csv = df.to_csv(index=False)
                b64 = base64.b64encode(csv.encode()).decode()
                href = f'<a href="data:file/csv;base64,{b64}" download="cleaned_data_{i + 1}.csv">Download cleaned_data_{i + 1}.csv</a>'
                st.markdown(href, unsafe_allow_html=True)
    else:
        st.warning("Please upload CSV file(s).")
        st.stop()
        
        

    st.markdown("")
    st.markdown("---")
    st.markdown("")
    st.markdown("<p style='text-align: center'><a href='https://github.com/shantanugondane/CleanSweep'>Github</a></p>", unsafe_allow_html=True)
if selected == "About":            
# Display some sample images from your dataset

    st.header("What is CLEANSWEEP ?")
  
    st.write("In an era driven by data-driven decision-making, the quality and reliability of the data you work with are paramount. Unfortunately, raw data often arrives in a state that requires careful handling and cleaning to be useful. Data cleaning is a crucial preliminary step in the data analysis pipeline. This project focuses on creating a user-friendly tool for data cleaning of CSV (Comma-Separated Values) files using Streamlit, a popular Python library for building web applications. Streamlit provides an interactive and intuitive platform for users to upload, preprocess, and clean their data, allowing for the seamless transformation of messy datasets into high-quality information. This project streamlines the data preparation process, making it more accessible and efficient for data analysts, scientists, and professionals across various domains.")
    st.write("This Streamlit-based data cleaning project offers a user-friendly interface for efficient CSV file processing. Users can upload multiple files, customize merging, and specify data cleaning options such as eliminating duplicates and empty rows. The tool visually presents cleaned dataframes and facilitates easy downloads in CSV format. This simplifies data preparation for analysts and professionals, enhancing data quality and usability. The About section provides insights into the project's significance, demonstrating its adaptability in various domains where clean, high-quality data is a prerequisite for informed decision-making and valuable insights. Streamlining the data cleaning process, this project promotes data accuracy and efficiency in analysis.")
    st.header("How it works ?")
    image = Image.open('data.jpg')
    st.image(image, caption='Fig : Process Flow of CleanSweep')
    st.write("This data cleaning project, powered by Streamlit, simplifies the process of preparing and cleaning CSV files. Users begin by uploading their data. They can select to merge multiple files or clean them individually, with options to remove duplicates, empty rows, and more. The tool displays the cleaned dataframes, allowing users to verify the results. Once satisfied, users can download the cleaned data in CSV format. This intuitive web application empowers users to efficiently clean and preprocess data, making it accessible to data analysts, scientists, and professionals from various fields, while also offering an About section for additional insights into its applications.")