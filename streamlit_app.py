
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
from adjustText import adjust_text

from constants import (
    COLUMN_COUNT,
    COLUMN_LETTER_DIMENSION_1, 
    COLUMN_LETTER_DIMENSION_2,
    COLUMN_CLUSTER,
    COLUMN_TOKEN,
    OUTPUT_LOCATION,    
    COLUMN_CASS_BRAND,
    COUNTRY_OFFERING,
    COLUMN_LABEL,
    COLUMN_PROBABILITY
)



def create_app():
    st.title('Brand Discoveries App')
    
    country = st.selectbox(
     'Select country data',
     (COUNTRY_OFFERING))

    # Create a text element and let the reader know the data is loading.
    data_load_state = st.text('Loading data...')

    data = pd.read_csv(OUTPUT_LOCATION.format(country))

    df = data.drop([COLUMN_LETTER_DIMENSION_1,COLUMN_LETTER_DIMENSION_2], axis=1)  
    
    #create_selection_box(df)
    # convert df to csv
    csv = df.to_csv().encode('utf-8')

    data_load_state.text('Loading data...done!')
    # create header in streamlit
    st.header('Extracted Tokens Dataset')

    st.dataframe(df)
    st.download_button(label="Download dataset as CSV file", data=csv, file_name=f'brand_discovery_{country}.csv')

    if set(COLUMN_LABEL).issubset(data.columns):
        map_character_simmilarities(data)

    else:
        map_character_simmilarities_no_label(data)

def map_character_simmilarities_no_label(df):

    
    st.header('Brand Groups')
    
    cluster_size = st.slider("Select size of Brand Clusters", min_value=2,max_value=10, value=(7,10),step=1)
    
    vc = df[COLUMN_CLUSTER].value_counts()
    df = df[df[COLUMN_CLUSTER].isin(vc[(vc >= cluster_size[0])&(vc <= cluster_size[1])].index)]
    
    fig = plt.figure(figsize=(25, 15))

    sns.scatterplot(data=df, x=COLUMN_LETTER_DIMENSION_1, y=COLUMN_LETTER_DIMENSION_2,hue=COLUMN_COUNT,  palette="viridis")

    texts = []
    
    def label_point(x, y, val, ax):
        a = pd.concat({'x': x, 'y': y, 'val': val}, axis=1)
        for i, point in a.iterrows():
            texts.append(ax.text(point['x']+.02, point['y'], str(point['val']), fontsize=9))

    label_point(df[COLUMN_LETTER_DIMENSION_1], df[COLUMN_LETTER_DIMENSION_2], df[COLUMN_TOKEN], plt.gca())
    adjust_text(texts, only_move={'points':'y', 'texts':'y'}, arrowprops=dict(arrowstyle="->", color='r', lw=0.5))
    
    st.pyplot(fig)
    st.balloons()



def map_character_simmilarities(df):

    
    st.header('Brand Groups')
    
    cluster_size = st.slider("Select size of Brand Clusters", min_value=2,max_value=10, value=(7,10),step=1)
    
    vc = df[COLUMN_CLUSTER].value_counts()
    df = df[df[COLUMN_CLUSTER].isin(vc[(vc >= cluster_size[0])&(vc <= cluster_size[1])].index)]
    
    fig = plt.figure(figsize=(25, 15))

    sns.scatterplot(data=df, x=COLUMN_LETTER_DIMENSION_1, y=COLUMN_LETTER_DIMENSION_2,hue=COLUMN_LABEL, size=COLUMN_COUNT, palette="viridis")

    texts = []
    
    def label_point(x, y, val, ax):
        a = pd.concat({'x': x, 'y': y, 'val': val}, axis=1)
        for i, point in a.iterrows():
            texts.append(ax.text(point['x']+.02, point['y'], str(point['val']), fontsize=9))

    label_point(df[COLUMN_LETTER_DIMENSION_1], df[COLUMN_LETTER_DIMENSION_2], df[COLUMN_TOKEN], plt.gca())
    adjust_text(texts, only_move={'points':'y', 'texts':'y'}, arrowprops=dict(arrowstyle="->", color='r', lw=0.5))
    
    st.pyplot(fig)
    st.balloons()



if __name__ == "__main__":
    create_app()


