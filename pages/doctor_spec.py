import streamlit as st
import base64
import pandas as pd
import os
from collections import Counter
from sklearn.preprocessing import LabelEncoder
from sklearn import tree, svm
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier

def get_base64_of_bin_file(image_path):
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

def set_background_for_theme(selected_palette="pink"):
    from core.theme import get_current_theme

    # --- Get current theme info ---
    current_theme = st.session_state.get("current_theme", None)
    if not current_theme:
        current_theme = get_current_theme()
    
    is_dark = current_theme["name"] == "Dark"

    # --- Map light themes to background images ---
    palette_color = {
        "light": "static_files/pink.png",
        "calm blue": "static_files/blue.png",
        "mint": "static_files/mint.png",
        "lavender": "static_files/lavender.png",
        "pink": "static_files/pink.png"
    }

    # --- Select background based on theme ---
    if is_dark:
        background_image_path = "static_files/dark.png"
    else:
        background_image_path = palette_color.get(selected_palette.lower(), "static_files/pink.png")

    encoded_string = get_base64_of_bin_file(background_image_path)
    st.markdown(
        f"""
        <style>
        /* Entire app background */
        html, body, [data-testid="stApp"] {{
            background-image: url("data:image/png;base64,{encoded_string}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}

        /* Main content transparency */
        .block-container {{
            background-color: rgba(255, 255, 255, 0);
        }}

        /* Sidebar: brighter translucent background */
        [data-testid="stSidebar"] {{
            background-color: rgba(255, 255, 255, 0.6);  /* Brighter and translucent */
            color: {'black' if is_dark else 'rgba(49, 51, 63, 0.8)'} ;  /* Adjusted for light background */
        }}

        /* Header bar: fully transparent */
        [data-testid="stHeader"] {{
            background-color: rgba(0, 0, 0, 0);
        }}

        /* Hide left/right arrow at sidebar bottom */
        button[title="Close sidebar"],
        button[title="Open sidebar"] {{
            display: none !important;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Force your own page config
st.set_page_config(
    page_title="Disease Predictor & Doctor Specialist Recommender",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ✅ Set your background image
selected_palette = st.session_state.get("palette_name", "Pink")
set_background_for_theme(selected_palette)

if 'selected_symptoms' not in st.session_state:
    st.session_state.selected_symptoms = []

# Custom light mode styles
st.markdown("""
    <style>
    /* Light mode */
    [data-theme="light"] body, [data-theme="light"] .stApp {
        background-color: #f9f9f9 !important;
        color: black !important;
    }

    /* Dark mode */
    [data-theme="dark"] body, [data-theme="dark"] .stApp {
        background-color: #0e1117 !important; /* Streamlit's dark background */
        color: white !important;
    }

    /* Buttons */
    .stButton>button {
        background: #4CAF50 !important;
        color: white !important;
        border-radius: 10px !important;
        font-size: 16px !important;
        height: 3em !important;
        width: 100% !important;
    }
    .stButton>button:hover { background: #45a049 !important; }

    /* Download button */
    .stDownloadButton>button {
        background-color: #2196F3 !important;
        color: white !important;
        border-radius: 8px !important;
        padding: 8px 16px !important;
    }
    .stDownloadButton>button:hover {
        background-color: #0b7dda !important;
    }

    /* Dataframe container */
    .stDataFrame {
        background-color: white !important;
        border-radius: 8px !important;
        padding: 8px !important;
    }

    /* Dark mode DataFrame */
    [data-theme="dark"] .stDataFrame {
        background-color: #1e222b !important;
        color: white !important;
    }

    /* Chart containers */
    .stPlotlyChart, .stAltairChart, .stVegaLiteChart {
        background-color: white !important;
        border-radius: 8px !important;
        padding: 10px !important;
    }
    [data-theme="dark"] .stPlotlyChart,
    [data-theme="dark"] .stAltairChart,
    [data-theme="dark"] .stVegaLiteChart {
        background-color: #1e222b !important;
        color: white !important;
    }
    </style>
""", unsafe_allow_html=True)

# Get base path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Load datasets
dis_sym_data = pd.read_csv(os.path.join(BASE_DIR, "Original_Dataset.csv"))
doc_data = pd.read_csv(os.path.join(BASE_DIR, "Doctor_Versus_Disease.csv"), encoding='latin1', names=['Disease', 'Specialist'])
des_data = pd.read_csv(os.path.join(BASE_DIR, "Disease_Description.csv"))

# Prepare symptom columns
columns_to_check = [col for col in dis_sym_data.columns if col != 'Disease']
symptoms_list = list(set(dis_sym_data.iloc[:, 1:].values.flatten()))
symptoms_list = [s for s in symptoms_list if pd.notna(s)]

for symptom in symptoms_list:
    dis_sym_data[symptom] = dis_sym_data.iloc[:, 1:].apply(lambda row: int(symptom in row.values), axis=1)

dis_sym_data_v1 = dis_sym_data.drop(columns=columns_to_check)
dis_sym_data_v1 = dis_sym_data_v1.loc[:, dis_sym_data_v1.columns.notna()]
dis_sym_data_v1.columns = dis_sym_data_v1.columns.str.strip()

# Encode labels
le = LabelEncoder()
dis_sym_data_v1['Disease'] = le.fit_transform(dis_sym_data_v1['Disease'])
X = dis_sym_data_v1.drop(columns="Disease")
y = dis_sym_data_v1['Disease']

# Train models
algorithms = {
    'Logistic Regression': LogisticRegression(),
    'Decision Tree': tree.DecisionTreeClassifier(),
    'Random Forest': RandomForestClassifier(),
    'SVM': svm.SVC(probability=True),
    'NaiveBayes': GaussianNB(),
    'K-Nearest Neighbors': KNeighborsClassifier(),
}
for model in algorithms.values():
    model.fit(X, y)

# Sidebar
st.sidebar.header("🛠️ Input Options")

# Symptom Grouping
symptom_groups_definition = {
    "Cardiovascular": [
        'fast heart rate', 'palpitations', 'swollen legs', 'swollen blood vessels', 'prominent veins on calf', 'chest pain'
    ],
    "Eyes": [
        'yellowing of eyes', 'blurred and distorted vision', 'redness of eyes', 'pain behind the eyes', 'sunken eyes', 'watering from eyes'
    ],
    "Gastrointestinal": [
        'stomach pain', 'acidity', 'ulcers on tongue', 'vomiting', 'indigestion', 'nausea', 'loss of appetite',
        'constipation', 'abdominal pain', 'diarrhoea', 'swelling of stomach', 'passage of gases', 'internal itching',
        'belly pain', 'increased appetite', 'stomach bleeding', 'distention of abdomen', 'excessive hunger',
        'pain during bowel movements', 'pain in anal region', 'bloody stool', 'irritation in anus'
    ],
    "Head, Throat, & Respiratory": [
        'continuous sneezing', 'patches in throat', 'cough', 'breathlessness', 'headache', 'phlegm',
        'throat irritation', 'sinus pressure', 'runny nose', 'congestion', 'loss of smell',
        'mucoid sputum', 'rusty sputum', 'blood in sputum'
    ],
    "Musculoskeletal": [
        'joint pain', 'muscle weakness', 'back pain', 'neck pain', 'knee pain', 'hip joint pain', 'swelling joints',
        'movement stiffness', 'painful walking', 'muscle pain', 'cramps'
    ],
    "Neurological & Mental": [
        'anxiety', 'mood swings', 'dizziness', 'slurred speech', 'loss of balance', 'unsteadiness',
        'spinning movements', 'altered sensorium', 'depression', 'irritability', 'lack of concentration',
        'visual disturbances', 'coma', 'restlessness'
    ],
    "Skin & General Appearance": [
        'itching', 'skin rash', 'nodal skin eruptions', 'yellowish skin', 'bruising', 'puffy face and eyes',
        'dischromic  patches', 'skin peeling', 'silver like dusting', 'small dents in nails',
        'inflammatory nails', 'blister', 'red sore around nose', 'yellow crust ooze', 'pus filled pimples',
        'blackheads', 'scurring', 'red spots over body', 'toxic look (typhos)'
    ],
    "Systemic & General": [
        'shivering', 'chills', 'fatigue', 'weight gain', 'weight loss', 'lethargy', 'high fever',
        'sweating', 'dehydration', 'mild fever', 'malaise', 'weakness in limbs', 'weakness of one body side',
        'muscle wasting', 'obesity', 'cold hands and feets'
    ],
    "Urinary": [
        'burning micturition', 'spotting  urination', 'dark urine', 'yellow urine', 'bladder discomfort',
        'foul smell of urine', 'continuous feel of urine', 'polyuria'
    ],
    "Other/Miscellaneous": [
        'irregular sugar level', 'acute liver failure', 'fluid overload', 'swelled lymph nodes',
        'enlarged thyroid', 'brittle nails', 'swollen extremeties', 'extra marital contacts',
        'drying and tingling lips', 'abnormal menstruation', 'family history', 'history of alcohol consumption',
        'receiving blood transfusion', 'receiving unsterile injections'
    ]
}

def clean_symptom_name(s):
    return s.strip().replace('_', ' ').replace('.1', '').replace('  ', ' ')

symptom_to_group_map = {}
for group, symptoms in symptom_groups_definition.items():
    for symptom in symptoms:
        symptom_to_group_map[symptom] = group

grouped_symptoms_in_data = {}
for symptom in symptoms_list:
    clean_symptom = clean_symptom_name(symptom)
    group = symptom_to_group_map.get(clean_symptom, "Other/Miscellaneous")
    if group not in grouped_symptoms_in_data:
        grouped_symptoms_in_data[group] = []
    grouped_symptoms_in_data[group].append(symptom)

for group in grouped_symptoms_in_data:
    grouped_symptoms_in_data[group].sort()
grouped_symptoms_in_data = dict(sorted(grouped_symptoms_in_data.items()))

search_query = st.sidebar.text_input("🔍 Search Symptoms", "", help="Type to search for symptoms across all categories.")

# Collect current selections from checkboxes
current_selection = []
symptom_container = st.sidebar.container()
with symptom_container:
    for group, symptoms_in_group in grouped_symptoms_in_data.items():
        symptoms_to_show = [s for s in symptoms_in_group if search_query.lower() in s.lower()] if search_query else symptoms_in_group
        if symptoms_to_show:
            with st.expander(group, expanded=bool(search_query)):
                for symptom in symptoms_to_show:
                    is_checked = st.checkbox(symptom, value=(symptom in st.session_state.selected_symptoms), key=symptom)
                    if is_checked:
                        current_selection.append(symptom)

st.session_state.selected_symptoms = current_selection
selected_symptoms = st.session_state.selected_symptoms

threshold = st.sidebar.slider("📊 Confidence threshold (%)", 0, 100, 20)
show_chart = st.sidebar.checkbox("📈 Show Probability Chart", value=True)

# Title
st.markdown("""
    <style>
    [data-theme="light"] h1.app-title {
        color: black !important;
    }
    [data-theme="dark"] h1.app-title {
        color: white !important;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown(
    "<h1 class='app-title' style='text-align: center;'>🩺 Disease Predictor & Doctor Specialist Recommender</h1>",
    unsafe_allow_html=True
)

# Prediction
if st.sidebar.button("🔎 Predict Disease"):
    if len(selected_symptoms) == 0:
        st.warning("⚠️ Please select at least one symptom!")
    else:
        with st.spinner("⏳ Analyzing symptoms and predicting..."):
            test_data = {col: 1 if col in selected_symptoms else 0 for col in X.columns}
            test_df = pd.DataFrame(test_data, index=[0])

            predicted = []
            for model_name, model in algorithms.items():
                pred = model.predict(test_df)
                disease = le.inverse_transform(pred)[0]
                predicted.append(disease)

            disease_counts = Counter(predicted)
            percentage_per_disease = {
                disease: (count / len(algorithms)) * 100 for disease, count in disease_counts.items()
            }

            percentage_per_disease = {d: p for d, p in percentage_per_disease.items() if p >= threshold}

            if len(percentage_per_disease) == 0:
                st.error("❌ No diseases met the confidence threshold!")
            else:
                result_df = pd.DataFrame({
                    "Disease": list(percentage_per_disease.keys()),
                    "Chances (%)": list(percentage_per_disease.values())
                })
                result_df = result_df.merge(doc_data, on='Disease', how='left')
                result_df = result_df.merge(des_data, on='Disease', how='left')

                st.markdown("### 📋 Prediction Results", unsafe_allow_html=True)

                # Iterate through results and display in a more readable format
                for index, row in result_df.iterrows():
                    with st.expander(f"**{row['Disease']}** ({row['Chances (%)']:.2f}% chance)"):
                        st.markdown(f"**⚕️ Recommended Specialist:** {row['Specialist']}")
                        st.markdown("**📖 Description:**")
                        st.write(row['Description'])

                st.markdown("---")  # Add a separator

                # Download button
                csv = result_df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 Download Results as CSV",
                    data=csv,
                    file_name="disease_predictions.csv",
                    mime="text/csv"
                )

                # Probability chart
                if show_chart:
                    st.markdown("### 📊 Probability Chart", unsafe_allow_html=True)
                    st.bar_chart(result_df.set_index("Disease")["Chances (%)"])
