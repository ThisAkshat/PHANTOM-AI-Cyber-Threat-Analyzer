import streamlit as st
from utils.predict import predict

st.set_page_config(page_title="PHANTOM - Cyber AI", page_icon="🛡️")

st.title("🛡️ PHANTOM")
st.subheader("AI Powered Cyber Threat Analyzer")

text = st.text_area("Paste Email, Message or URL")

if st.button("Analyze"):
    if text.strip() == "":
        st.warning("Enter some text")
    else:
        label, conf = predict(text) 

        if label == "phishing":
            st.error("🚨 PHISHING DETECTED")
        else:
            st.success("✅ SAFE")

        st.write("Confidence:", round(conf * 100, 2), "%")
   

