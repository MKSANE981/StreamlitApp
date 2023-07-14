import streamlit as st
import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image

import statistics as stat
ensae=Image.open('ensae.png')
st.set_page_config(page_title="ENSAE - Mansour Kama SANE", page_icon=ensae, layout="wide")
col1, col2 = st.columns([1,5])
with col1:
    st.image(ensae)
with col2:
    st.title("Application de chargement et de fusion de base")


uploaded_files = st.file_uploader("Choose a CSV file", accept_multiple_files=True)
data_frames = []  # Liste pour stocker les DataFrames importés
options = []
base_names = []
today = datetime.datetime.now()
container = st.container()
@st.cache_data
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')
# Parcourir les fichiers téléchargés
a=0
fusion = None  # Variable pour stocker la base de données fusionnée
for uploaded_file in uploaded_files:
    # Lire le fichier CSV et ajouter le DataFrame à la liste
    df = pd.read_csv(uploaded_file)
    df=pd.DataFrame(df)
    nom = uploaded_file.name.split(".")[0]
    df[nom] = uploaded_file.name.split(".")[0]
    #st.dataframe(df,use_container_width=True)
    ## Supprimer la variable dont le nom contient fusion_
    df = df.filter(regex=r'^(?!.*fusion_).*$', axis=1)
    data_frames.append(df)
    base_names.append(uploaded_file.name)

# Vérifier si des fichiers ont été téléchargés
if data_frames:
    with st.sidebar:
        # Créer une liste des noms de fichiers
        file_names = [uploaded_file.name for uploaded_file in uploaded_files]
        # Afficher les noms des fichiers dans la barre latérale
        st.sidebar.header("Fichiers téléchargés :")
        options = st.multiselect('Selectionner une base', file_names)
        # Vérifier si une base de données est sélectionnée
# Afficher les bases de données sélectionnées
    if options:
        st.header("Données sélectionnées :")
    for option in options:
        index = file_names.index(option)  # Récupérer l'index de la base sélectionnée
        selected_df = data_frames[index]  # Récupérer le DataFrame correspondant
        st.write(option)
        #st.write(selected_df)  # Afficher le DataFrame
        st.dataframe(selected_df, use_container_width=True)

    with st.sidebar:
        data_merge = st.multiselect('Merger les données', file_names,max_selections=2)
        st.write("Attention, même nom pour var de merge!")
        nom_var=[]
        if len(data_merge)>1:
            bases=[]
            base_names=[]
            for base_selected in data_merge:
                index = file_names.index(base_selected)  # Récupérer l'index de la base sélectionnée
                selected_df = data_frames[index]  # Récupérer le DataFrame correspondant
                bases.append(selected_df)
                base_names.append(base_selected)
                for column in selected_df.columns:
                    nom_var.append(column)
            # Utilisation de la fonction unique() de NumPy pour obtenir les éléments uniques et leurs compteurs
            elements, compteurs = np.unique(nom_var, return_counts=True)
            # Filtrer les éléments répétés plus de deux fois
            nom_var_merge = elements[compteurs >1]
            variable_merge = st.selectbox("Variable de merge",nom_var_merge)
            if variable_merge:
                if st.button("Merger"):
                    if len(bases[1]) < len(bases[0]):
                        fusion = pd.merge(bases[0], bases[1],how="left", on=variable_merge)
                    else:
                        fusion = pd.merge(bases[1], bases[0], how="left", on=variable_merge)
                    csv = convert_df(fusion)
                    nom = "fusion_" + base_names[0].split(".")[0] + "_" + base_names[1].split(".")[0] + ".csv"
                    with container:
                        st.download_button(
                            label="Download data as CSV",
                            data=csv,
                            file_name=nom,
                            mime='text/csv',
                        )
                        # st.write(fusion)
                        st.dataframe(fusion, use_container_width=True)
                        st.title("Visualisation des données")
                        base_visual = st.multiselect('Sélectionner', base_names)
















