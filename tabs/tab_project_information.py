import streamlit as st
from PIL import Image


def create(data, metadata, cfg):

    with open("dashboard.md", "r", encoding="utf-8") as f:
        md = f.read()

    st.markdown(md)
    systemoverview = Image.open("data/REMix_flexmex_example.png")
    st.image(systemoverview, output_format="png")
