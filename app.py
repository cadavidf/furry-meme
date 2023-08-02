import pandas as pd
import streamlit as st
import plotly.express as px
from PIL import Image

st.set_page_config(page_title='Animality Dashboard')
# --- DISPLAY IMAGE & DATAFRAME
col1, col2 = st.columns(2)

# --- DEFINE YOUR COLOR SEQUENCE
color_sequence = ['#232323', '#525252', '#251513', '#1c88aa', '#1c82ad']

image = Image.open('animality logotype official.png')
print(image)
col1.image(image, caption='Designed by Felipe Cadavid', use_column_width=100)

st.header('DEMO')

st.subheader('⦁This is an dashboard of an internal survey from X company employees ranking of an activity.')
st.subheader('⦁Determine preferences aming gropus by moving the slider between the 23yr/o and the 63yr/o')
st.subheader('⦁Add or remove departments to filter by department.')

st.header('Move the slider to select data')

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

department_selection = st.multiselect('Department:',
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
group_color = {i: '1c88aa' for i in subset}


# --- PLOT BAR CHART
bar_chart = px.bar(df_grouped,
                   x='Rating',
                   y='Votes',
                   text='Votes',
                   color_discrete_sequence=color_sequence*len(df_grouped), 
                   template='plotly_white')
st.plotly_chart(bar_chart)


#col1.dataframe(df[mask])

# --- PLOT PIE CHART
pie_chart = px.pie(df_participants,
                title='Total No. of Participants',
                values='Participants',
                color='Departments',
                color_discrete_sequence= px.colors.qualitative.Alphabet,
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
