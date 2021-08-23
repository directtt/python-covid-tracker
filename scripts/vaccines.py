import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from scripts import today as td


def parse_data():
    columns = ['wojewodztwo', 'liczba_szczepien_ogolnie', 'liczba_szczepien_dziennie',
               'dawka_2_ogolem', 'dawka_2_dziennie']
    data = pd.read_csv('datasets/vaccines_data.csv', encoding='windows-1250', sep=';', usecols=columns)
    data = data[data['wojewodztwo'] != 'inne_puste_woj']
    population = {'dolnośląskie': 2898525,
                  'kujawsko-pomorskie': 2069273,
                  'lubelskie': 2103342,
                  'lubuskie': 1010177,
                  'łódzkie': 2448713,
                  'małopolskie': 3413931,
                  'mazowieckie': 5428031,
                  'opolskie': 980771,
                  'podkarpackie': 2125901,
                  'podlaskie': 1176576,
                  'pomorskie': 2346717,
                  'śląskie': 4508078,
                  'świętokrzyskie': 1230044,
                  'warmińsko-mazurskie': 1420514,
                  'wielkopolskie': 3500361,
                  'zachodniopomorskie': 1693219,
                  'cały kraj': 0}

    data['ludnosc'] = data.wojewodztwo.map(population)
    data.loc[data['wojewodztwo'] == 'cały kraj', 'ludnosc'] = data['ludnosc'].sum()
    data['zaszczepieni [%]'] = data['dawka_2_ogolem'] / data['ludnosc']
    perc = lambda x: "{:.2%}".format(x)
    data['zaszczepieni [%]'] = data['zaszczepieni [%]'].apply(perc)

    return data


def app():
    td.download_data('https://www.arcgis.com/sharing/rest/content/items/0b17f540e23e4871a1196fd4097f9659/data', 'vaccines_data.csv')
    data = parse_data()

    today = data.iloc[-1, :]
    today.name = 'data'
    states = data.iloc[:-1, :].sort_values('zaszczepieni [%]', ascending=False)

    st.dataframe(data=today)
    st.dataframe(data=states)

    states['plot_val'] = states['zaszczepieni [%]'].str[:5].astype(float)
    states.sort_values('plot_val', inplace=True)
    plt.style.use('seaborn')
    fig = plt.figure()
    ax = plt.axes()
    ax.barh(states['wojewodztwo'], states['plot_val'], edgecolor="black", linewidth=1)
    ax.set_ylabel('Województwo')
    ax.set_xlabel('Zaszczepiona ludność [%]')
    td.autolabel(ax.patches, ax, '%g', 1.6)
    st.pyplot(fig, dpi=100)
