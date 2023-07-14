import streamlit as st
import pandas as pd
import numpy as np
import datetime
from PIL import Image
from st_pages import Page, show_pages, add_page_title

# Optional -- adds the title and icon to the current page
add_page_title("ENSAE Dakar - Cours de ML2")

# Specify what pages should be shown in the sidebar, and what their titles and icons
# should be
show_pages(
    [
        Page("main_file.py", "Page d'accueil", "🏠"),
        Page("mansour_api.py","Chargement et fusion de base", ":open_file_folder:"),
        Page("other_pages/dashboard.py", "Visualisation", ":bar_chart:"),
    ]
)