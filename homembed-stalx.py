import streamlit as st
import pandas as pd
import plotly.express as px
from io import StringIO

# Création d'un jeu de données fictif
data = {
    'Date': pd.date_range(start='2024-01-01', periods=12, freq='ME'),
    'Budget': [100, 120, 110, 130, 150, 140, 160, 180, 170, 190, 200, 210],
    'Forecast1': [90, 110, 100, 120, 140, 130, 150, 170, 160, 180, 190, 200],
    'Forecast2': [95, 105, 115, 125, 145, 135, 155, 175, 165, 185, 195, 205],
    'Actual': [80, 100, 95, 115, 135, 125, 145, 165, 155, 175, 185, 195]
}

df = pd.DataFrame(data)
df = df.set_index('Date')

# Streamlit App
st.set_page_config(page_icon=None, layout="wide", initial_sidebar_state="collapsed", menu_items=None)
# st.title("Analyse Budgétaire")

# Diviser la page en deux colonnes
col1, col2 = st.columns(2, gap="small")

with col1 :
    edited_df = st.data_editor(df, height=(12 + 1) * 35 + 3)

# Afficher le DataFrame sous forme de texte modifiable dans la première colonne
new_data = edited_df.to_csv(index=True)

# Mettre à jour le DataFrame depuis le texte
new_df = pd.read_csv(StringIO(new_data), index_col='Date')

# Sélection du scenario avec Picker dans la deuxième colonne
with col2 :
    selected_scenario = st.radio(
        "Choisissez le scenario à analyser :",
        ["Budget", "Forecast1", "Forecast2"], index=0, key="scenario_selection", horizontal=True
    )

# Création du graphique dans la deuxième colonne avec lissage des courbes et couleurs spécifiques
fig = px.line(new_df, x=new_df.index, y=[selected_scenario, 'Actual'],
              labels={'value': 'Montant', 'variable': 'Scénario'},
              line_shape='spline', line_dash_sequence=['solid', 'solid'])

# Définition des couleurs spécifiques
colors = {'Actual': '#9e8aea', selected_scenario: '#d6c7ff'}

# Mise à jour des couleurs
for i, trace in enumerate(fig.data):
    trace.line.color = colors[trace.name]
    trace.line.width = 3  # Épaisseur de la ligne

# Mise à jour du layout
fig.update_layout(title_text=f"Comparaison {selected_scenario} vs Actual",
                  xaxis_title='Date', yaxis_title='Montant cumulé (k euros)', showtoolbar=False)

# Affichage du graphique dans la deuxième colonne
col2.plotly_chart(fig)
