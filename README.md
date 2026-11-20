
# Hospital Appointment Operations Analysis

**Project 9 | Healthcare Operations | Python, NumPy and Pandas**

## 1. Overview

An individual, entry-level data analytics project that analyzes synthetic hospital appointment records to understand appointment trends, attendance patterns, waiting times, department performance and estimated consultation revenue.

The project uses Python, NumPy, Pandas and data visualization libraries to perform data cleaning, statistical analysis and generate operational recommendations.

## 2. Dataset

**File:** `data/09_hospital_appointments_100_records.csv`

- Total records: 100 synthetic appointment records
- Total columns: 9
- Domain: Healthcare Operations
- Data type: Synthetic operational data
- Clinical or personal medical information: Not included

### Dataset Columns

1. `Appointment_ID`
2. `Patient_ID`
3. `Appointment_Date`
4. `Department`
5. `Appointment_Type`
6. `Attendance_Status`
7. `Waiting_Time_Minutes`
8. `SMS_Reminder`
9. `Consultation_Fee`

## 3. Project Objectives

- Inspect and understand hospital appointment records.
- Identify and handle duplicate records.
- Handle missing waiting-time values.
- Calculate total appointments and attendance percentages.
- Compare average waiting times across departments.
- Identify departments with higher no-show percentages.
- Analyze the relationship between SMS reminders and no-show rates.
- Compare consultation fees across departments.
- Analyze appointment volumes by date and department.
- Compare waiting times for new and follow-up appointments.
- Calculate statistical measures using NumPy.
- Identify waiting-time outliers using the IQR method.
- Categorize waiting times.
- Estimate consultation fees from attended appointments.
- Provide five operational recommendations.

## 4. Technologies and Libraries

- Python 3
- NumPy
- Pandas
- Matplotlib
- Seaborn
- Jupyter Notebook

### Installation

Install the required libraries using:

```bash
pip install numpy pandas matplotlib seaborn jupyter
```

## 5. Project Structure

```text
Hospital_Appointment_Operations_Analysis/
│
├── SRS/
│   └── Project_9_Hospital_Appointment_Operations_SRS.docx
│
├── src/
│   ├── analysis.ipynb
│   └── analysis.py
│
├── data/
│   └── 09_hospital_appointments_100_records.csv
│
└── README.md
```

## 6. How to Run the Project

### Option 1: Jupyter Notebook

1. Clone or download this repository.
2. Open the project folder in VS Code or a terminal.
3. Install the required libraries.
4. Start Jupyter Notebook:

```bash
jupyter notebook
```

5. Open `src/analysis.ipynb`.
6. Run all cells in sequence.

### Option 2: Python Script

Run the standalone Python analysis script from the project root:

```bash
python src/analysis.py
```

The notebook and Python script use the project dataset through relative-path handling.

## 7. Data Cleaning and Methodology

The following data-cleaning rules are applied:

- Duplicate `Appointment_ID` records are identified and reported.
- The first occurrence of a duplicate appointment ID is retained.
- Missing waiting times for cancelled and no-show appointments are left missing because waiting time is not applicable.
- Missing waiting times for attended appointments are imputed using the median waiting time of the corresponding department.
- An imputation indicator is maintained to identify imputed values.
- Waiting-time outlier analysis is performed on attended appointments only.

## 8. Analysis Performed

The project covers:

- Appointment and attendance analysis.
- Department-wise average waiting-time analysis.
- Department-wise no-show rate comparison.
- SMS reminder comparison.
- Department-wise average consultation fees.
- Date-wise and department-wise appointment volume.
- New versus follow-up appointment comparison.
- NumPy statistical analysis, including median, quartiles and standard deviation.
- IQR-based outlier detection.
- Waiting-time categorization.
- Estimated consultation fees from attended appointments.

## 9. Scope and Limitations

- The dataset is synthetically generated for educational purposes.
- It does not represent actual hospital records.
- The analysis is descriptive and does not establish causal relationships.
- SMS reminder comparisons do not prove that reminders cause changes in attendance.
- Estimated attended fees assume that the listed consultation fee is earned for every attended appointment.
- Actual payment, refund and collection information is unavailable.
- No clinical or medical conclusions should be drawn.

## 10. Expected Outcome

The project demonstrates how Python, NumPy and Pandas can be used to analyze operational data, identify appointment trends, understand waiting-time patterns and support data-driven operational recommendations.

## 11. Author Information

- **Student Name:** Sanchit Singh Negi
- **Student ID:** 2026B15410200
- **Course:** B.Tech CSE (Data Science)
- **Semester:** First Semester
- **College:** ABES Engineering College
- **Academic Session:** 2026–27
- **Project:** Project 9 — Hospital Appointment Operations Analysis

---

**Academic Project | ABES Engineering College | 2026–27**

