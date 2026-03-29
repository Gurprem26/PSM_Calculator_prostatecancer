import streamlit as st

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Prostate Cancer PSM Risk Calculator", page_icon="🩺", layout="centered")

# --- CUSTOM COLOR HEADER ---
st.markdown("<h1 style='text-align: center; color: #1E3A8A;'>The PSM Risk Calculator</h1>", unsafe_allow_html=True)

# Use an info box for a colorful, professional introduction
st.info("""
**Predicting Positive Surgical Margins (PSM) in Robotic-Assisted Radical Prostatectomy (RARP)** This calculator utilizes exact Shapley Additive Explanations (SHAP) weights derived from an optimized Random Forest architecture (N=757). It calculates the patient's risk by adding their individualized SHAP impacts to the baseline institutional PSM prevalence (20.3%).
""")

st.divider()

# --- INPUT SECTION ---
st.markdown("<h3 style='color: #0F766E;'>Patient & Clinical Parameters</h3>", unsafe_allow_html=True)

# Reordered to strictly follow: Age -> BMI -> PSA -> Cores -> GG -> Imaging
col1, col2 = st.columns(2)

with col1:
    st.markdown("**Demographics & Labs**")
    # Options are now strictly sequential
    age = st.selectbox("Patient Age", ["< 60", "60 - 70", "> 70"])
    bmi = st.selectbox("Patient BMI", ["< 25 (Normal)", ">= 25 (Overweight/Obese)"])
    psa = st.selectbox("Preoperative PSA (ng/mL)", ["<= 10.0", "> 10.0"])
    
with col2:
    st.markdown("**Biopsy Pathology**")
    cores = st.selectbox("Percentage of Positive Cores", ["< 10%", "10% - 50%", "> 50%"])
    gg = st.selectbox("Biopsy Grade Group", ["GG 1", "GG 2", "GG 3", "GG 4", "GG 5"])

st.markdown("<br><h3 style='color: #0F766E;'>Advanced Preoperative Imaging</h3>", unsafe_allow_html=True)
col3, col4 = st.columns(2)

with col3:
    suv = st.selectbox("PSMA PET SUVmax", ["< 5.0", "5.0 - 10.0", "> 10.0"])
with col4:
    mri = st.selectbox("MRI Clinical Stage", ["Organ Confined (Favorable)", "Borderline/Equivocal", "Definite EPE/Locally Advanced"])


# --- EXACT SHAP WEIGHT LOGIC ---
shap_sum = 0.0

# 1. Age
if age == "< 60": shap_sum += -0.0060
elif age == "60 - 70": shap_sum += 0.0057
elif age == "> 70": shap_sum += -0.0343

# 2. BMI
if bmi == "< 25 (Normal)": shap_sum += 0.0070
elif bmi == ">= 25 (Overweight/Obese)": shap_sum += -0.0258

# 3. PSA
if psa == "<= 10.0": shap_sum += -0.0765  
elif psa == "> 10.0": shap_sum += -0.0004

# 4. Biopsy Cores
if cores == "< 10%": shap_sum += -0.0763
elif cores == "10% - 50%": shap_sum += -0.0389
elif cores == "> 50%": shap_sum += 0.0482

# 5. Gleason Grade Group
if gg == "GG 1": shap_sum += -0.0180
elif gg == "GG 2": shap_sum += -0.0252
elif gg == "GG 3": shap_sum += -0.0076
elif gg == "GG 4": shap_sum += 0.0190
elif gg == "GG 5": shap_sum += 0.0636

# 6. PSMA PET CT SUVmax
if suv == "< 5.0": shap_sum += -0.0350
elif suv == "5.0 - 10.0": shap_sum += -0.0102
elif suv == "> 10.0": shap_sum += 0.0124

# 7. MRI
if mri == "Organ Confined (Favorable)": shap_sum += -0.0310
elif mri == "Borderline/Equivocal": shap_sum += -0.0007
elif mri == "Definite EPE/Locally Advanced": shap_sum += 0.1194

# --- FINAL PROBABILITY CALCULATION ---
BASE_RATE = 0.203  # 20.3% Institutional Baseline
final_probability = BASE_RATE + shap_sum

# Bound the probability between 0% and 100%
final_probability_percent = max(0.0, min(100.0, final_probability * 100))

# --- DCA-DERIVED RISK STRATIFICATION ---
st.divider()
st.markdown("<h2 style='text-align: center; color: #1E3A8A;'>Risk Stratification & Clinical Recommendation</h2>", unsafe_allow_html=True)

# Display the main metric prominently
st.metric(
    label="Predicted Probability of Positive Surgical Margin (PSM)", 
    value=f"{final_probability_percent:.1f}%"
)

st.markdown("<p style='text-align: center; color: gray;'><em>(Risk strata determined by Decision Curve Analysis net-benefit thresholds)</em></p>", unsafe_allow_html=True)
st.write("") # Spacer

# Color-coded action blocks based on DCA thresholds
if final_probability_percent <= 12.0:
    st.success("""
    ### 🟢 LOW RISK (< 12%)
    **Clinical Context:** The predicted risk falls below the DCA action threshold. The model yields a highly reliable Negative Predictive Value (NPV).
    
    **Surgical Recommendation:** Safe to proceed with **bilateral intrafascial nerve-sparing** to maximize functional recovery.
    """)

elif final_probability_percent <= 25.0:
    st.warning("""
    ### 🟡 INTERMEDIATE RISK (12% - 25%)
    **Clinical Context:** The predicted risk falls within the DCA net-benefit zone. There is moderate biological or anatomical risk of extraprostatic extension.
    
    **Surgical Recommendation:** Exercise caution. Consider **unilateral or interfascial nerve-sparing** targeted away from the ipsilateral side of dominant MRI/PET lesions.
    """)

else:
    st.error("""
    ### 🔴 HIGH RISK (> 25%)
    **Clinical Context:** The predicted risk exceeds the upper DCA threshold. The risk of leaving residual microscopic disease mathematically outweighs the functional benefits of nerve preservation.
    
    **Surgical Recommendation:** Prioritize maximum oncological control. **Wide excision / non-nerve-sparing approach** strongly recommended.
    """)

st.divider()
st.caption("Disclaimer: This tool is for peer-reviewed academic demonstration and should not replace independent clinical judgment. External validation pending.")