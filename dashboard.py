import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import datetime
from PIL import Image
ensae=Image.open('ensae.png')
st.set_page_config(page_title="ENSAE - Mansour Kama SANE", page_icon=ensae, layout="wide")
st.set_option('deprecation.showPyplotGlobalUse', False)
col1, col2 = st.columns([1,5])
with col1:
    st.image(ensae)
with col2:
    st.title("Dashboard📊")

##########################################################################################################
##                  Définition de quelques fonctions de filtre et de construction der graphique

# Filtrer les données en fonction de ce qui est sélectionné
@st.cache_data
def apply_filters(df, campaign_ids, age_range, date_range):
    filtered_df = df.copy()
    # Filtre sur l'identifiant de campagne (campaign_id)
    if campaign_ids:
        filtered_df = filtered_df[filtered_df["campaign_id"].isin(campaign_ids)]

    # Filtre sur l'âge (age)
    if len(age_range):
        filtered_df = filtered_df[(filtered_df["age"] >= age_range[0]) & (filtered_df["age"] <= age_range[1])]

    # Filtre sur la date (timestamp_x)
    if date_range:
        filtered_df = filtered_df[filtered_df["timestamp_x"].isin(date_range)]
    return filtered_df


# Calculer le chiffre d'affaires
def calculate_revenue(df):
    revenue = df["price"].sum()
    return revenue


# Créer le box plot de l'âge en fonction du produit acheté
def create_age_product_boxplot(df):
    filtered_data = df #.dropna(subset=["age", "product_id"])
    plt.figure(figsize=(10, 6))
    sns.boxplot(x="product_id", y="age", data=filtered_data)
    plt.xlabel("Produit acheté")
    plt.ylabel("Âge")
    plt.title("Box Plot de l'Âge en fonction du Produit Acheté")
    st.pyplot()


# Créer le diagramme en barre des clics en fonction du temps
def create_clicks_time_barplot(df):
    filtered_data = df#.dropna(subset=["timestamp_x"])
    counts = filtered_data["timestamp_x"].value_counts()
    plt.figure(figsize=(10, 6))
    counts.plot(kind="bar")
    plt.xlabel("Temps")
    plt.ylabel("Nombre de clics")
    plt.title("Diagramme en Barre des Clics en fonction du Temps")
    st.pyplot()


# Créer l'entonnoir de conversion
def create_conversion_funnel(df):
    st.write("Entonnoir de Conversion")
    achats_total = df["achats"].count()
    impressions_total = df["impressions"].count()
    clics_total = df["clics"].count()

    fig_achats = go.Funnel(
        y=["Impressions", "Clics", "Achats"],
        x=[impressions_total, clics_total, achats_total],
        textposition="inside",
        textinfo="value+percent previous",
        marker=dict(color="teal"),
    )

    # Personnaliser le layout du graphique
    layout = go.Layout(
        title="Entonnoir",
        margin=dict(l=50, r=50, t=80, b=50),
    )
    st.plotly_chart(go.Figure(data=[fig_achats], layout=layout))

    #st.write([achats_total,impressions_total,clics_total])

def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')
##########################################################################################################

uploaded_file = st.file_uploader("Choose a CSV file", accept_multiple_files=False)
donnees_reduites=[]
if uploaded_file:
    # Lire le fichier CSV et ajouter le DataFrame à la liste
    df = pd.read_csv(uploaded_file)
    df=pd.DataFrame(df)
    #data_frames.append(df)
    voir_base = st.checkbox("Voir la base")
    if voir_base:
        st.dataframe(df, use_container_width=True)
    elements, compteurs = np.unique(df.columns, return_counts=True)
    col1,col2 = st.columns([4,1])
    with col1:
        variables = st.multiselect("Variable à conserver dans la suite",elements)
    with col2:
        if variables:
            donnees_reduites = df[variables]
    if variables:
        with st.container():
            st.dataframe(donnees_reduites,use_container_width=True)
    if "timestamp_x" in variables:
        if st.checkbox('Conversion de la variable date'):
            donnees_reduites['timestamp_x'] = pd.to_datetime(donnees_reduites["timestamp_x"], unit="s").dt.strftime("%d-%m-%Y")
            col1, col2 = st.columns(2)
            with col1:
                st.write('Conversion effectuée avec succès!')
            with col2:
                csv = convert_df(donnees_reduites)
                nom = "base_finale.csv"
                st.download_button(
                    label="Download data as CSV",
                    data=csv,
                    file_name=nom,
                    mime='text/csv',
                )
            #st.dataframe(donnees_reduites, use_container_width=True)
    if len(donnees_reduites)>1:
        # Barre latérale pour les filtres
        st.sidebar.title("Filtres")
        campaign_ids = st.sidebar.multiselect("Sélectionner l'identifiant de campagne (campaign_id)",
                                              donnees_reduites["campaign_id"].unique())
        age_range = []
        col1,col2 = st.columns(2)
        with col1:
            filtre_age = st.sidebar.checkbox("Age")
        with col2:
            if filtre_age:
                age_range = st.sidebar.slider("Sélectionner la plage d'âge", min_value=int(donnees_reduites["age"].min()),
                                      max_value=int(donnees_reduites["age"].max()),
                                      value=(int(donnees_reduites["age"].min()), int(donnees_reduites["age"].max())))
        date_range = st.sidebar.multiselect("Filtrer par dates", donnees_reduites["timestamp_x"].unique())
        #st.write(date_range)
        # Appliquer les filtres
        filtered_data = apply_filters(donnees_reduites, campaign_ids, age_range, date_range)
        lig11,lig12 = st.columns(2)
        with lig11:
            st.write("Sortie 1")
            # Afficher le chiffre d'affaires
            revenue = calculate_revenue(filtered_data)
            st.title(f"Chiffre d'affaires total : {revenue} €")
        with lig12:
            st.write("Sortie 2")
            create_clicks_time_barplot(filtered_data)


        lig21, lig22 = st.columns(2)

        with lig21:
            st.write("Sortie 3")
            create_age_product_boxplot(filtered_data)
        with lig22:
            st.write("Sortie 4")
            create_conversion_funnel(filtered_data)
            #st.write(filtered_data["achats"].count(), filtered_data["impressions"].count(), filtered_data["clics"].count())
