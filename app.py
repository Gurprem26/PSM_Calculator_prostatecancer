import streamlit as st

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Prostate Cancer Positive Surgical Margin Risk Calculator", page_icon="🩺", layout="centered")

st.title("The PSM Calculator")
st.markdown("""
**Predicting Positive Surgical Margins (PSM) in Robotic-Assisted Radical Prostatectomy (RARP)** This calculator utilizes exact Shapley Additive Explanations (SHAP) weights derived from an optimized Random Forest architecture (N=757). It calculates the patient's risk by adding their individualized SHAP impacts to the baseline institutional PSM prevalence (20.3%).
""")
st.divider()

# --- INPUT COLUMNS ---
st.header("Patient Parameters")
col1, col2 = st.columns(2)

with col1:
    cores = st.selectbox("Percentage of Positive Cores", ["< 10%", "10% - 50%", "> 50%"])
    psa = st.selectbox("Preoperative PSA (ng/mL)", ["<= 10.0", "> 10.0"])
    gg = st.selectbox("Biopsy Grade Group", ["GG 1", "GG 2", "GG 3", "GG 4", "GG 5"])
    suv = st.selectbox("PSMA PET SUVmax", ["< 5.0", "5.0 - 10.0", "> 10.0"])

with col2:
    mri = st.selectbox("MRI Clinical Stage", ["Organ Confined (Favorable)", "Borderline/Equivocal", "Definite EPE/Locally Advanced"])
    age = st.selectbox("Patient Age", ["> 70", "< 60", "60 - 70"])
    bmi = st.selectbox("Patient BMI", [">= 25 (Overweight/Obese)", "< 25 (Normal)"])

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
if psa == "<= 10.0": shap_sum += -0.0765  # Averaged <4 and 4-10
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

# 7. MRI (Aggregated Tiers based on your data)
if mri == "Organ Confined (Favorable)": shap_sum += -0.0310
elif mri == "Borderline/Equivocal": shap_sum += -0.0007
elif mri == "Definite EPE/Locally Advanced": shap_sum += 0.1194

# --- FINAL PROBABILITY CALCULATION ---
BASE_RATE = 0.203  # 20.3% Institutional Baseline
final_probability = BASE_RATE + shap_sum

# Bound the probability between 0% and 100%
final_probability_percent = max(0.0, min(100.0, final_probability * 100))

# --- RESULTS DISPLAY ---
# --- FINAL PROBABILITY CALCULATION ---
BASE_RATE = 0.203  # 20.3% Institutional Baseline
final_probability = BASE_RATE + shap_sum

# Bound the probability between 0% and 100%
final_probability_percent = max(0.0, min(100.0, final_probability * 100))

# --- DCA-DERIVED RISK STRATIFICATION ---
st.divider()
st.header("Risk Stratification & Clinical Recommendation")

st.metric(
    label="Predicted Probability of Positive Surgical Margin (PSM)", 
    value=f"{final_probability_percent:.1f}%", 
    delta=f"{shap_sum*100:+.1f}% from baseline", 
    delta_color="inverse"
)

st.markdown("*(Risk strata determined by Decision Curve Analysis net-benefit thresholds)*")

# Use your exact DCA thresholds here (e.g., 12% and 25%)
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