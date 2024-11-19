import pandas as pd
import plotly.express as px
import warnings
import streamlit as st

warnings.filterwarnings("ignore")

data = pd.read_csv("ladesaeulen.csv", delimiter=";")


def app():
    st.title("Die Betreiber der öffentlichen Ladesäulen in Deutschland")

    st.subheader("Ladesäulenbetreiber - Anteile (Andere Betreiber: Betreiber mit weniger als 200 Ladesäulen)")

    betreiber_group = data.groupby("Betreiber").size().reset_index(name= 'Anzahl')
    betreiber_group.loc[betreiber_group['Anzahl'] < 200, 'Betreiber'] = 'Andere Betreiber'
    betreiber_group = betreiber_group.sort_values(by='Anzahl', ascending=False).reset_index(drop=True)
    betreiber_group.index += 1

    fig = px.pie(betreiber_group, 
                names='Betreiber', 
                values='Anzahl', 
                color_discrete_sequence=px.colors.sequential.Viridis,
                height=400)

    st.plotly_chart(fig)

    st.divider()

    col1, col2 = st.columns(2)

    with col1:

        top_ten_betreiber = betreiber_group.head(10)
        st.subheader("Die TOP 10 - Betreiber mit den meisten Ladesäulen")
        st.write(top_ten_betreiber)



    with col2:
        betreiber_group_haupt = betreiber_group.loc[betreiber_group['Betreiber'] != 'Andere Betreiber']

        fig = px.bar(betreiber_group_haupt.sort_values(by='Anzahl'), 
                    x='Anzahl', 
                    y='Betreiber', 
                    color='Anzahl',
                    height=600,
                    orientation='h',
                    color_discrete_sequence=px.colors.sequential.Blues_r)
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig)







