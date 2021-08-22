import pandas as pd
import requests
import streamlit as st
from selenium import webdriver
import matplotlib.pyplot as plt


def get_download_url(url):
    op = webdriver.ChromeOptions()
    op.add_argument('headless')
    browser = webdriver.Chrome(options=op)
    browser.implicitly_wait(5)  # gives an implicit wait for 5 seconds to load the website
    browser.get(url)

    download_url = browser.find_element_by_xpath('//*[@id="ember53"]/b/a').get_attribute('href')
    browser.quit()
    return download_url


def download_data(download_url, name):
    req = requests.get(download_url)
    path = 'D:/polish-covid-tracker/datasets/' + name
    with open(path, 'wb') as f:
        f.write(req.content)


def parse_data():
    cols = ['wojewodztwo', 'liczba_przypadkow', 'zgony', 'liczba_ozdrowiencow',
            'liczba_wykonanych_testow', 'liczba_osob_objetych_kwarantanna', 'stan_rekordu_na']
    data = pd.read_csv('datasets/todays_data.csv', sep=';', encoding='windows-1250', usecols=cols)
    data['stan_rekordu_na'] = pd.to_datetime(data['stan_rekordu_na']).dt.strftime('%d.%m.%y')
    data.insert(6, 'cases/tests[%]', data['liczba_przypadkow'] / data['liczba_wykonanych_testow'])
    perc = lambda x: "{:.2%}".format(x)
    data['cases/tests[%]'] = data['cases/tests[%]'].apply(perc)
    data = data.convert_dtypes()
    data['cases/tests[%]'] = data['cases/tests[%]'].astype("string")

    return data


def autolabel(rects, ax, formatting, cut):
    """
    Attach a text label above each bar displaying its height
    """
    for rect in rects:
        width = rect.get_width()
        ax.text(rect.get_x() + rect.get_width() - cut, rect.get_y() + rect.get_height()/2.,
                formatting % width,
                ha='center', va='center', color='white')


def app():
    download_data(get_download_url('https://wojewodztwa-rcb-gis.hub.arcgis.com/pages/dane-do-pobrania'), 'todays_data.csv')
    data = parse_data()
    today = data.iloc[0, 1:]
    today.name = 'data'
    states = data.iloc[1:, :-1]

    st.write("""
    ## Today's COVID-19 statistics in Poland.
    (source: gov.pl)
    """)

    st.dataframe(data=today)
    st.dataframe(data=states.sort_values('liczba_przypadkow', ascending=False))

    states.sort_values('liczba_przypadkow', inplace=True)
    plt.style.use('seaborn')
    fig = plt.figure()
    ax = plt.axes()
    ax.barh(states['wojewodztwo'], states['liczba_przypadkow'], edgecolor="black", linewidth=1)
    ax.set_ylabel('Województwo')
    ax.set_xlabel('Liczba przypadków')
    autolabel(ax.patches, ax, '%d', 0.6)
    st.pyplot(fig, dpi=100)
