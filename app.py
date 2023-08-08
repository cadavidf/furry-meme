import pandas as pd
import streamlit as st
import random
import plotly.express as px
from PIL import Image

st.set_page_config(page_title='Animality Dashboard')
# --- DISPLAY IMAGE & DATAFRAME
col1, col2 = st.columns(2)

# --- DEFINE YOUR COLOR SEQUENCE
color_sequence = ['#15ACD5', '#1af3aa', '#251513', '#1c88aa', '#1c82ad']

image = Image.open('animality logotype official.png')
print(image)
col1.image(image, caption='B2B Solutions for Businesses', use_column_width=100)

st.header('DEMO')

st.text('⦁This is an dashboard of an internal survey')
st.subheader('Title: Employee Ranking Company Activities')
st.text('⦁Determine preferences aming gropus by moving the slider between the 23yr/o and the 63yr/o')
st.text('⦁Add or remove departments to filter by department.')

st.header('Select Age Range & Departments')
st.text('move slider <--->')

### --- LOAD DATAFRAME

excel_file = 'Survey_Results.xlsx'
sheet_name = 'DATA'

df = pd.read_excel(excel_file,
                   sheet_name=sheet_name,
                   usecols='B:D',
                   header=3)

df_participants = pd.read_excel(excel_file,
                                sheet_name= sheet_name,
                                usecols='F:G',
                                header=3)
df_participants.dropna(inplace=True)

# --- STREAMLIT SELECTION
department = df['Department'].unique().tolist()
ages = df['Age'].unique().tolist()

age_selection = st.slider('Age:',
                        min_value= min(ages),
                        max_value= max(ages),
                        value=(min(ages),max(ages)))

department_selection = st.multiselect('Add or Remove Departments by clicking on the X.',
                                    department,
                                    default=department)

# --- FILTER DATAFRAME BASED ON SELECTION
mask = (df['Age'].between(*age_selection)) & (df['Department'].isin(department_selection))
number_of_result = df[mask].shape[0]
st.markdown(f'*Available Results: {number_of_result}*')

# --- GROUP DATAFRAME AFTER SELECTION
df_grouped = df[mask].groupby(by=['Rating']).count()[['Age']]
df_grouped = df_grouped.rename(columns={'Age': 'Votes'})
df_grouped = df_grouped.reset_index()
subset = {"Finance", "Marketing", "Sales", "Logistics", "Purchasing"}
colors = ['#1c82ad', '#328eb5', '#499bbd', '#60a7c5', '#76b4cd', '#8dc0d6', '#f7b176', '#f79e50', '#f7882c', '#f7720a']

group_color = {department: color for department, color in zip(subset, colors)}

# --- PLOT BAR CHART
bar_chart = px.bar(df_grouped,
                   x='Rating',
                   y='Votes',
                   text='Votes',
                   color_discrete_sequence=color_sequence*len(df_grouped), 
                   template='plotly_white')
st.plotly_chart(bar_chart)


#col1.dataframe(df[mask])
colors_pie = ['#499bbd', '#60a7c5', '#76b4cd', '#8dc0d6', '#f7b176', '#f79e50', '#f7882c', '#f7720a']
random.shuffle(colors_pie)
shuffled_colors_pie = colors_pie[:]

# --- PLOT PIE CHART
pie_chart = px.pie(df_participants,
                title='Total No. of Participants',
                values='Participants',
                color='Departments',
                color_discrete_sequence= shuffled_colors_pie,
                color_discrete_map= group_color,
                names='Departments')

st.plotly_chart(pie_chart)

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)
