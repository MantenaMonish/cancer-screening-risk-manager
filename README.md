
# Cancer Screening Reminder System

This project is a machine learning-based system that helps generate personalized cancer screening reminders for patients based on their medical history, lifestyle, and existing risk labels. The pipeline includes data preprocessing, exploratory data analysis (EDA), model training, and screening schedule generation based on clinical guidelines.

This project is a full-stack application that helps healthcare professionals identify patients at risk for breast, cervical, and colorectal cancer and generate timely screening reminders.

It includes:
- A **backend (Flask API)** for risk prediction and reminder logic
- A **frontend (React)** for dashboard visualization and interaction
- A **machine learning pipeline** that trains models for each cancer type
- Integration with patient data (`patients.csv`) for real-time inference

---
## Project Structure

- **Data Loading and Cleaning**  
  Cleans the patient dataset by parsing dates, filling missing values, and engineering features such as smoking status, alcohol consumption, obesity, and family history.

- **Exploratory Data Analysis (EDA)**  
  Visualizes distributions, risk level imbalances, missing values, and feature correlations to understand data behavior.

- **Risk Stratification Models**  
  Trains a separate Random Forest classifier for each cancer type:
  - Breast Cancer
  - Cervical Cancer
  - Colorectal Cancer

- **Screening Guidelines**  
  Determines the next screening interval based on the patient’s gender, age, and risk level using clinical rules.

- **Reminder System**  
  Generates reminders for patients whose next screening date falls within a specified window.

## Dataset

The dataset (`patients.csv`) includes:
- Demographic data (age, gender)
- Family history
- Lifestyle indicators (smoking, alcohol, obesity)
- Past screening dates
- Risk labels (Low, Medium, High) for three cancer types

Sample columns:
- `patient_id`, `name`, `age`, `gender`
- `family_history`, `lifestyle`
- `last_breast_screen`, `last_cervical_screen`, `last_colorectal_screen`
- `risk_breast`, `risk_cervical`, `risk_colorectal`

## How to Run

1. Install dependencies:
   ```bash
   pip install pandas numpy scikit-learn matplotlib seaborn
