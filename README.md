# Prostate Cancer Positive Surgical Margin Risk Calculator

**Authors:** Gurpremjit Singh, et al.  

## Overview
This repository hosts the clinical calculator designed to predict the risk of Positive Surgical Margins (PSM) prior to Robotic-Assisted Radical Prostatectomy (RARP). 

This tool utilizes the exact Shapley Additive Explanations (SHAP) weights derived from an optimized, multimodal Random Forest machine learning architecture evaluated on a cohort of 757 patients. By integrating standard clinicopathological data with advanced preoperative imaging (mpMRI and PSMA PET/CT), it provides an individualized, mathematically precise probability of PSM.

## Decision Curve Analysis (DCA) Risk Stratification
Actionable risk tiers were established using Decision Curve Analysis (DCA) to maximize clinical net benefit:
* **Low Risk (≤ 12%):** Ideal candidate for bilateral intrafascial nerve-sparing (High NPV).
* **Intermediate Risk (13% - 25%):** Consider unilateral or interfascial nerve-sparing.
* **High Risk (> 25%):** Prioritize oncological control; wide excision / non-nerve-sparing recommended.

## Live Web Application
The calculator is hosted live via Streamlit Community Cloud and can be accessed on any desktop or mobile device: 
👉 **[Insert your Streamlit App URL here once deployed]**

*(Disclaimer: This tool is for peer-reviewed academic demonstration and should not replace independent clinical judgment).*