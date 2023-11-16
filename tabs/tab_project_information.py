import streamlit as st
from PIL import Image


def create(data, metadata, cfg):

    with open("dashboard.md", "r", encoding="utf-8") as f:
        md = f.read()

    st.markdown(md)
    systemoverview = Image.open("data/flexmex-scenarios.jpg")
    st.image(systemoverview, output_format="jpg")
    systemoverview = Image.open("data/flexmex-model-scope.jpg")
    st.image(systemoverview, output_format="jpg")
