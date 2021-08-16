# import pandas as pd
# import requests
# import streamlit as st
# from selenium import webdriver
# import matplotlib.pyplot as plt
#
# # TODO: graphs on streamlit
# # TODO: display whole summary with .csv file on streamlit
# # TODO: eventually vaccined
#
#
# def get_download_url(url):
#     op = webdriver.ChromeOptions()
#     op.add_argument('headless')
#     browser = webdriver.Chrome(options=op)
#     browser.implicitly_wait(5)  # gives an implicit wait for 5 seconds to load the website
#     browser.get(url)
#
#     download_url = browser.find_element_by_xpath('//*[@id="ember53"]/b/a').get_attribute('href')
#     browser.quit()
#     return download_url
#
#
# def download_data(download_url):
#     req = requests.get(download_url)
#     path = 'D:/polish-covid-tracker/datasets/todays_data.csv'
#     with open(path, 'wb') as f:
#         f.write(req.content)
#
#
# def parse_data():
#     cols = ['wojewodztwo', 'liczba_przypadkow', 'zgony', 'liczba_ozdrowiencow',
#             'liczba_wykonanych_testow', 'liczba_osob_objetych_kwarantanna', 'stan_rekordu_na']
#     data = pd.read_csv('datasets/todays_data.csv', sep=';', encoding='windows-1250', usecols=cols)
#     data['stan_rekordu_na'] = pd.to_datetime(data['stan_rekordu_na']).dt.strftime("%d.%m.%y")
#     data.insert(6, 'cases/tests[%]', data['liczba_przypadkow'] / data['liczba_wykonanych_testow'])
#     perc = lambda x: "{:.2%}".format(x)
#     data['cases/tests[%]'] = data['cases/tests[%]'].apply(perc)
#     data = data.convert_dtypes()
#     data['cases/tests[%]'] = data['cases/tests[%]'].astype("string")
#
#     return data
#
#
# def parse_complete_data():
#     complete_data = pd.read_csv('datasets/complete_data.csv', encoding='windows-1250')
#     # complete_data['date'] = pd.to_datetime(complete_data['date']).dt.strftime("%d.%m.%y")
#     # complete_data['cases/tests[%]'] = complete_data['new_cases'] / complete_data['new_tests']
#     # perc = lambda x: "{:.2%}".format(x)
#     # complete_data['cases/tests[%]'] = complete_data['cases/tests[%]'].apply(perc)
#
#     return complete_data
#
#
# def update_complete_data(complete_data, today_data):
#     new_row = {'date': today_data['stan_rekordu_na'], 'total_cases': complete_data.iloc[-1, 1] + today_data['liczba_przypadkow'],
#                    'new_cases': today_data['liczba_przypadkow'], 'total_deaths': complete_data.iloc[-1, 3] + today_data['zgony'],
#                    'new_deaths': today_data['zgony'], 'new_tests': today_data['liczba_wykonanych_testow'],
#                    'cases/tests[%]': today_data['cases/tests[%]']}
#
#     complete_data = complete_data.append(new_row, ignore_index=True)
#     complete_data.to_csv('datasets/complete_data.csv', index=False)
#     return complete_data
#
# # def autolabel(rects):
# #     """
# #     Attach a text label above each bar displaying its height
# #     """
# #     for rect in rects:
# #         width = rect.get_width()
# #         ax.text(rect.get_x() + rect.get_width() - 0.5, rect.get_y() + rect.get_height()/2.,
# #                 '%d' % width,
# #                 ha='center', va='center', color='white')
#
#
# if __name__ == '__main__':
#     # download_data(get_download_url('https://wojewodztwa-rcb-gis.hub.arcgis.com/pages/dane-do-pobrania'))
#
#     data = parse_data()
#     complete_data = parse_complete_data()
#
#     today = data.iloc[0, 1:]
#     today.name = 'data'
#     states = data.iloc[1:, :-1]
#     if today['stan_rekordu_na'] not in complete_data['date'].tolist():
#         complete_data = update_complete_data(complete_data, today)
#
#     print(complete_data.tail(10).to_string())
#
#     # st.title('Polish COVID-19 Tracker')
#
#     # st.write("""
#     # ## Today's Coronavirus statistics in Poland.
#     # (source: gov.pl)
#     # """)
#     #
#     # st.dataframe(data=today)
#     # st.dataframe(data=states.sort_values('liczba_przypadkow', ascending=False))
#     #
#     # states.sort_values('liczba_przypadkow', inplace=True)
#     # plt.style.use('seaborn')
#     # fig = plt.figure()
#     # ax = plt.axes()
#     # ax.barh(states['wojewodztwo'], states['liczba_przypadkow'], edgecolor="black", linewidth=1)
#     # ax.set_ylabel('Województwo')
#     # ax.set_xlabel('Liczba przypadków')
#     # autolabel(ax.patches)
#     # st.pyplot(fig, dpi=100)
#
#     # st.write("""
#     # ## Complete COVID-19 statistics in Poland.
#     # """)
#     # st.dataframe(data=complete_data.sort_index(ascending=False))