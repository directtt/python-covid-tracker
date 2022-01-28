import pandas as pd
import requests
import streamlit as st
import plotly.express as px
from selenium import webdriver


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
    path = 'datasets/' + name
    with open(path, 'wb') as f:
        f.write(req.content)


def parse_data(path):
    cols = ['wojewodztwo', 'liczba_przypadkow', 'zgony', 'liczba_ozdrowiencow',
            'liczba_wykonanych_testow', 'liczba_osob_objetych_kwarantanna', 'stan_rekordu_na']
    data = pd.read_csv(path, sep=';', encoding='windows-1250', usecols=cols)
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
    download_data('https://www.arcgis.com/sharing/rest/content/items/153a138859bb4c418156642b5b74925b/data', 'todays_data.csv')
    data = parse_data('datasets/todays_data.csv')
    today = data.iloc[0, 1:]
    today.name = 'data'
    states = data.iloc[1:, :-1]

    st.write("""
    ## Today's COVID-19 statistics in Poland.
    (source: gov.pl)
    """)

    st.dataframe(data=today)
    st.dataframe(data=states.sort_values('liczba_przypadkow', ascending=False))

    states.sort_values('liczba_przypadkow', inplace=True, ascending=True)

    fig1 = px.bar(states,
                  x='liczba_przypadkow',
                  y='wojewodztwo',
                  orientation='h',
                  color='liczba_przypadkow',
                  color_continuous_scale=px.colors.sequential.Blues,
                  opacity=0.8,
                  # title='Value Count of Subject Types',
                  labels={
                      'liczba_przypadkow': 'Liczba przypadków',
                      'wojewodztwo': 'Województwo'})
    fig1.update_traces(marker_line_color='black',
                       marker_line_width=1)
    fig1.update_layout(width=850, height=550)
    st.write(fig1)

    fig2 = px.pie(states,
                  values='liczba_przypadkow',
                  names='wojewodztwo',
                  hole=0.5,
                  color_discrete_sequence=px.colors.sequential.Blues_r,
                  title='Liczba przypadków w województwach [%]')
    fig2.update_layout(width=800, height=550)
    st.write(fig2)

    # old plot
    # plt.style.use('seaborn')
    # fig = plt.figure()
    # ax = plt.axes()
    # ax.barh(states['wojewodztwo'], states['liczba_przypadkow'], edgecolor="black", linewidth=1)
    # ax.set_ylabel('Województwo')
    # ax.set_xlabel('Liczba przypadków')
    # autolabel(ax.patches, ax, '%d', 1)
    # st.pyplot(fig, dpi=100)
