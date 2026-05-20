# =========================================
# SALES EFFECTIVENESS ANALYSIS SYSTEM
# =========================================

import streamlit as st
import pandas as pd
import joblib
import re
from datetime import datetime


# =========================================
# PAGE CONFIG
# =========================================

st.set_page_config(
    page_title="Sales Effectiveness Analysis",
    page_icon="📊",
    layout="wide"
)

# =========================================
# CUSTOM CSS
# =========================================

st.markdown("""
<style>

.stApp{
    background-color:#0f172a;
    color:white;
}

h1,h2,h3,h4,h5,h6,p,label{
    color:white !important;
}

.stTextInput input,
.stNumberInput input{
    background-color:#1e293b !important;
    color:white !important;
    border-radius:12px !important;
    border:1px solid #334155 !important;
}

.stSelectbox div[data-baseweb="select"]{
    background-color:#1e293b !important;
    color:white !important;
    border-radius:12px !important;
}

.stButton>button{
    background-color:#2563eb;
    color:white;
    border:none;
    border-radius:12px;
    height:52px;
    width:260px;
    font-size:18px;
    font-weight:bold;
}

.stButton>button:hover{
    background-color:#1d4ed8;
}

.result-box{
    background-color:#111827;
    padding:30px;
    border-radius:18px;
    border-left:6px solid #2563eb;
    margin-top:30px;
}

</style>
""", unsafe_allow_html=True)

# =========================================
# HEADER
# =========================================

st.markdown("""

<div style="
background:linear-gradient(90deg,#0f172a,#1e293b);
padding:30px;
border-radius:18px;
margin-bottom:25px;
">

<h1 style="
text-align:center;
font-size:38px;
color:white;
">
📊 Sales Effectiveness Analysis
</h1>

<p style="
text-align:center;
font-size:18px;
color:#cbd5e1;
">
Machine Learning Based Lead Prediction System
</p>

</div>

""", unsafe_allow_html=True)

# =========================================
# LOAD MODEL
# =========================================

best_model = None

try:

    best_model = joblib.load(
        "xgboost_Model.pkl"
    )

except FileNotFoundError:

    st.error("❌ xgboost_Model.pkl not found")

except Exception as e:

    st.error(f"❌ Error loading model : {e}")

# =========================================
# DROPDOWN VALUES
# =========================================

sources = [

    "Website",
    "Call",
    "Live Chat-Direct",
    "Live Chat-Google Organic",
    "Live Chat-Google Ads",
    "Live Chat-Blog",
    "Live Chat-PPC",
    "Live Chat-Adwords Remarketing",
    "Live Chat-CPC",
    "By Recommendation",
    "Customer Referral",
    "Existing Client",
    "E-Mail Message"

]

sales_agents = [

    "Sales-Agent-3",
    "Sales-Agent-4",
    "Sales-Agent-7",
    "Sales-Agent-8",
    "Sales-Agent-9",
    "Sales-Agent-10",
    "Sales-Agent-11"

]

locations = [

    "Chennai",
    "Bangalore",
    "Hyderabad",
    "Delhi",
    "Mumbai",
    "Pune",
    "Kolkata",
    "Trivandrum",
    "UAE",
    "USA",
    "UK",
    "AUSTRALIA",
    "Singapore",
    "Other Locations"

]

delivery_modes = [

    "Mode-1",
    "Mode-2",
    "Mode-3",
    "Mode-4",
    "Mode-5"

]

# =========================================
# VALIDATION FUNCTIONS
# =========================================

def valid_mobile(mobile):

    pattern = r'^[0-9]{10}$'

    return re.fullmatch(pattern, mobile)

def valid_email(email):

    pattern = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'

    return re.fullmatch(pattern, email)

# =========================================
# INPUT SECTION
# =========================================

col1, col2 = st.columns(2)

# =========================================
# LEFT COLUMN
# =========================================

with col1:

    st.subheader("📋 Verification Information")

    Created = st.text_input(
        "Created Date",
        placeholder="DD-MM-YYYY"
    )

    Product_ID = st.number_input(
        "Product ID",
        min_value=0,
        step=1
    )

    Mobile = st.text_input(
        "Mobile Number"
    )

    EMAIL = st.text_input(
        "Email Address"
    )

# =========================================
# RIGHT COLUMN
# =========================================

with col2:

    st.subheader("📈 Lead Information")

    Source = st.selectbox(
        "Lead Source",
        ["Select Source"] + sources
    )

    Sales_Agent = st.selectbox(
        "Sales Agent",
        ["Select Sales Agent"] + sales_agents
    )

    Location = st.selectbox(
        "Location",
        ["Select Location"] + locations
    )

    Delivery_Mode = st.selectbox(
        "Delivery Mode",
        ["Select Delivery Mode"] + delivery_modes
    )

# =========================================
# BUTTON
# =========================================

st.markdown("<br>", unsafe_allow_html=True)

b1, b2, b3 = st.columns([1,1,1])

with b2:

    predict_btn = st.button(
        "Predict Lead Category"
    )

# =========================================
# PREDICTION
# =========================================

if best_model is not None and predict_btn:

    try:

        # =========================================
        # VALIDATIONS
        # =========================================

        if Source == "Select Source":

            st.warning("⚠️ Please select Lead Source")
            st.stop()

        if Sales_Agent == "Select Sales Agent":

            st.warning("⚠️ Please select Sales Agent")
            st.stop()

        if Location == "Select Location":

            st.warning("⚠️ Please select Location")
            st.stop()

        if Delivery_Mode == "Select Delivery Mode":

            st.warning("⚠️ Please select Delivery Mode")
            st.stop()

        # =========================================
        # MOBILE VALIDATION
        # =========================================

        if not valid_mobile(Mobile):

            st.error(
                "❌ Mobile Number Must Be Exactly 10 Digits"
            )

            st.stop()

        # =========================================
        # EMAIL VALIDATION
        # =========================================

        if not valid_email(EMAIL):

            st.error(
                "❌ Invalid Email Address"
            )

            st.stop()

        # =========================================
        # MODEL INPUT
        # =========================================

        input_data = pd.DataFrame({

            'Created': [Created],

            'Source': [Source],

            'Sales_Agent': [Sales_Agent],

            'Location': [Location],

            'Delivery_Mode': [Delivery_Mode]

        })

        # =========================================
        # MODEL PREDICTION
        # =========================================

        prediction = best_model.predict(
            input_data
        )[0]

        # =========================================
        # OUTPUT LABEL
        # =========================================

        if prediction == 1:

            result = "🟢 High Potential Lead"

        else:

            result = "🔴 Low Potential Lead"

        # =========================================
        # RESULT UI
        # =========================================

        st.markdown(f"""

        <div class="result-box">

        <h2 style="
        color:white;
        margin-bottom:20px;
        text-align:center;
        ">
        Prediction Result
        </h2>

        <p style="
        color:#60a5fa;
        font-size:36px;
        font-weight:bold;
        margin-top:25px;
        text-align:center;
        ">
        {result}
        </p>

        </div>

        """, unsafe_allow_html=True)

    except Exception as e:

        st.error(
            f"❌ Prediction Error : {e}"
        )

# =========================================
# FOOTER
# =========================================

st.markdown("""

<hr>

<div style="
text-align:center;
color:gray;
padding:10px;
">

Developed with ❤️ using Streamlit & Machine Learning

</div>

""", unsafe_allow_html=True)
