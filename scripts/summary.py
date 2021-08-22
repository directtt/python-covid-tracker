import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import base64
from scripts import today as td


def parse_complete_data():
    complete_data = pd.read_csv('datasets/complete_data.csv', encoding='windows-1250')
    # skip lines below, cause file is already saved in that format
    # complete_data['date'] = pd.to_datetime(complete_data['date']).dt.strftime("%d.%m.%y")
    # complete_data['cases/tests[%]'] = complete_data['new_cases'] / complete_data['new_tests']
    # perc = lambda x: "{:.2%}".format(x)
    # complete_data['cases/tests[%]'] = complete_data['cases/tests[%]'].apply(perc)

    return complete_data


def update_complete_data(complete_data, today_data):
    new_row = {'date': today_data['stan_rekordu_na'], 'total_cases': complete_data.iloc[-1, 1] + today_data['liczba_przypadkow'],
                   'new_cases': today_data['liczba_przypadkow'], 'total_deaths': complete_data.iloc[-1, 3] + today_data['zgony'],
                   'new_deaths': today_data['zgony'], 'new_tests': today_data['liczba_wykonanych_testow'],
                   'cases/tests[%]': today_data['cases/tests[%]']}

    complete_data = complete_data.append(new_row, ignore_index=True)
    complete_data.to_csv('datasets/complete_data.csv', index=False)
    return complete_data


def file_download(complete_data):
    csv = complete_data.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
    href = f'<a href="data:file/csv;base64,{b64}" download="complete_data.csv">Download CSV File</a>'

    return href


def app():

    complete_data = parse_complete_data()
    data = td.parse_data()
    today = data.iloc[0, 1:]
    plot_data = complete_data[['date', 'new_cases']]
    plot_data['date'] = pd.to_datetime(plot_data['date'], format='%d.%m.%y').dt.date
    plot_data['7day_rolling_avg'] = plot_data.new_cases.rolling(7).mean()
    # plot_data.sort_values(by='date', inplace=True)

    if today['stan_rekordu_na'] not in complete_data['date'].tolist():
        complete_data = update_complete_data(complete_data, today)

    st.write("""
        ## Complete COVID-19 statistics in Poland.
        (source: gov.pl)
        """)

    st.dataframe(data=complete_data.sort_index(ascending=False))

    st.markdown(file_download(complete_data), unsafe_allow_html=True)

    fig = plt.figure()
    ax = plt.axes()
    ax.plot(plot_data['date'], plot_data['7day_rolling_avg'])
    ax.set_title('Liczba nowych przypadków od początku trwania pandemii (średnia 7-dniowa)')
    ax.fill_between(plot_data['date'], plot_data['7day_rolling_avg'], alpha=0.30)
    ax.set_ylabel('Liczba przypadków')
    ax.set_xlabel('Data')
    ax.tick_params(axis='x', labelrotation=40)
    st.pyplot(fig, dpi=100)
