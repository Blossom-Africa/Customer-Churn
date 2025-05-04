import streamlit as st
import joblib
import numpy as np

# Load trained model
model = joblib.load("model.pkl")

# -------- Streamlit Page Config --------
st.set_page_config(page_title="Telco Churn Predictor", layout="centered", page_icon="📈")

# -------- Custom Styling to Hide Default Header --------
st.markdown("""
    <style>
        header {visibility: hidden;}  /* Hide default header */
    </style>
""", unsafe_allow_html=True)

# -------- Custom CSS Styling --------
st.markdown("""
    <style>
        /* Gradient Background */
        .stApp {
            background: linear-gradient(135deg, #031a47, #49c3fb);
            color: white;
        }

        /* Title and Subtitle */
        h1 {
            text-align: center;
            font-size: 4rem;
            font-weight: 900;
            color: white;
            margin-bottom: 1.5rem;
        }
        .subtitle {
            text-align: center;
            font-size: 1.2rem;
            color: #FBF8DA;
            margin-bottom: 2rem;
        }

        /* Form input text */
        label {
            color: black !important;
        }

        /* Adjust color for input fields */
        .stTextInput, .stSelectbox, .stNumberInput, .stSlider {
            background-color: #e0f7fa!important;
            color: black !important;
            border-radius: 12px;
        }

        /* Button styling */
        .stButton>button {
            background-color: #49c3fb;
            color: #031a47;
            font-weight: bold;
            border-radius: 10px;
            padding: 0.8rem 2rem;
        }

        .stButton>button:hover {
            background-color: #31a2d1;
        }

        /* Sidebar text color */
        .css-1cpxqw2 {
            color: white !important;
        }

        /* Remove footer */
        footer {
            visibility: hidden;
        }
    </style>
""", unsafe_allow_html=True)
# -------- Footer --------
st.markdown("""
    <style>
        .footer {
            position: fixed;
            bottom: 0;
            left: 0;
            width: 100%;
            background-color: #031a47;  /* Dark color for footer */
            color: #49c3fb;  /* Light blue text color */
            text-align: center;
            padding: 5px;
            font-size: 0.8rem;  /* Smaller font size */
            font-weight: normal;
        }
    </style>

    <div class="footer">
        Built by Akoma Intelligence
    </div>
""", unsafe_allow_html=True)


# -------- Title Section --------
st.markdown("<h1 class='title'> 📈 Telco Customer Churn Predictor</h1>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Fill out the form below to check if a customer is likely to churn.</div>", unsafe_allow_html=True)

# -------- Form Layout --------
with st.form("churn_form"):
    customerID = st.text_input("🔑 Customer ID")

    col1, col2 = st.columns(2)

    with col1:
        Dependents = st.selectbox("👨‍👩‍👧‍👦 Dependents", ["Yes", "No"])
        InternetService = st.selectbox("🌐 Internet Service", ["DSL", "Fiber optic", "No"])
        PaperlessBilling = st.selectbox("📩 Paperless Billing", ["Yes", "No"])
        MonthlyCharges = st.number_input("💵 Monthly Charges", min_value=0.0, max_value=500.0, step=1.0)

    with col2:
        tenure = st.slider("📅 Tenure (months)", 0, 72, 12)
        PhoneService = st.selectbox("📞 Phone Service", ["Yes", "No"])
        Contract = st.selectbox("📃 Contract", ["Month-to-month", "One year", "Two year"])
        PaymentMethod = st.selectbox("💳 Payment Method", [
            "Electronic check", "Mailed check", "Bank transfer (automatic)", "Credit card (automatic)"
        ])

    submit = st.form_submit_button("✨ Predict Churn")


# -------- Encoding Function --------
def encode_input(val, col):
    mapping = {
        'Dependents': {'Yes': 1, 'No': 0},
        'PhoneService': {'Yes': 1, 'No': 0},
        'InternetService': {'DSL': 0, 'Fiber optic': 1, 'No': 2},
        'Contract': {'Month-to-month': 0, 'One year': 1, 'Two year': 2},
        'PaperlessBilling': {'Yes': 1, 'No': 0},
        'PaymentMethod': {
            'Electronic check': 0,
            'Mailed check': 1,
            'Bank transfer (automatic)': 2,
            'Credit card (automatic)': 3
        }
    }
    return mapping[col][val]

# -------- Prediction Logic --------
if submit:
    input_data = np.array([[ 
        encode_input(Dependents, 'Dependents'),
        tenure,
        encode_input(PhoneService, 'PhoneService'),
        encode_input(InternetService, 'InternetService'),
        encode_input(Contract, 'Contract'),
        encode_input(PaperlessBilling, 'PaperlessBilling'),
        encode_input(PaymentMethod, 'PaymentMethod'),
        MonthlyCharges
    ]])

    prediction = model.predict(input_data)[0]

    if prediction == 1:
        st.error(f"⚠️ Customer `{customerID}` is **likely to churn**.")
    else:
        st.success(f"✅ Customer `{customerID}` is **unlikely to churn**.")
