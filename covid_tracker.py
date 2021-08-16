import streamlit as st
from multiapp import MultiApp
from scripts import summary, today

app = MultiApp()

st.title('Polish COVID-19 Tracker')

app.add_app('Today', today.app)
app.add_app('Summary', summary.app)

app.run()
