import streamlit as st
import pandas as pd
import plotly.express as px

# Création d'un jeu de données fictif
data = {
    'Date': pd.date_range(start='2024-01-01', periods=12, freq='M'),
    'Budget': [100, 120, 110, 130, 150, 140, 160, 180, 170, 190, 200, 210],
    'Forecast1': [90, 110, 100, 120, 140, 130, 150, 170, 160, 180, 190, 200],
    'Forecast2': [95, 105, 115, 125, 145, 135, 155, 175, 165, 185, 195, 205],
    'Actual': [80, 100, 95, 115, 135, 125, 145, 165, 155, 175, 185, 195]
}

df = pd.DataFrame(data)
df = df.set_index('Date')

# Streamlit App
st.title("Analyse Budgétaire")

# Sélection du scenario avec Picker
selected_scenario = st.selectbox("Choisissez le scenario à analyser :", ['Budget', 'Forecast1', 'Forecast2'])

# Création du graphique avec lissage des courbes et couleurs spécifiques
fig = px.line(df, x=df.index, y=[selected_scenario, 'Actual'], labels={'value': 'Montant', 'variable': 'Scénario'},
              line_shape='spline', line_dash_sequence=['solid', 'solid'])

# Définition des couleurs spécifiques
colors = {'Actual': '#9e8aea', selected_scenario: '#d6c7ff'}

# Mise à jour des couleurs
for i, trace in enumerate(fig.data):
    trace.line.color = colors[trace.name]
    trace.line.width = 2  # Épaisseur de la ligne

# Mise à jour du layout
fig.update_layout(title_text=f"Comparaison {selected_scenario} vs Actual",
                  xaxis_title='Date', yaxis_title='Montant cumulé (k euros)')

# Affichage du graphique
st.plotly_chart(fig)