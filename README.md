# Project 9: Hospital Appointment Operations Analysis

## Overview
An individual entry-level data analyst project using Python, NumPy and Pandas to analyze synthetic hospital appointment operations.

## Dataset
`data/09_hospital_appointments_100_records.csv`  
100 synthetic records, 9 columns. The dataset contains operational fields only and no clinical information.

## Project structure
```text
Hospital_Appointment_Operations_Analysis/
├── SRS/
│   └── Project_9_Hospital_Appointment_Operations_SRS.docx
├── src/
│   └── analysis.ipynb
├── data/
│   └── 09_hospital_appointments_100_records.csv
└── README.md
```

## Requirements
- Python 3
- pandas
- numpy
- matplotlib
- seaborn
- jupyter

Install:
```bash
pip install pandas numpy matplotlib seaborn jupyter
```

## Run the project
1. Download or clone this repository.
2. Open a terminal in the repository root.
3. Start Jupyter:
   ```bash
   jupyter notebook
   ```
4. Open `src/analysis.ipynb` and run all cells.

The notebook includes a relative-path fallback for running from either the project root or the `src` folder.

## Data-cleaning rules
- Duplicate `Appointment_ID` rows are reported; the first occurrence is retained for analysis.
- Missing waiting times for non-attended appointments are left missing because a waiting time is not applicable.
- Missing waiting times for attended appointments are imputed with the median for that department, and an imputation flag is kept.
- IQR outlier analysis uses attended appointments only.

## Scope and limitations
This is synthetic teaching data, not actual hospital information. The results are descriptive and do not establish causation. Estimated attended fees assume that the listed fee is earned for every attended appointment. No clinical conclusions should be drawn.

## Author
Student: [Enter your name]  
Student ID: [Enter your student ID]  
Course: B.Tech CSE (Data Science)  
Project: 9 — Hospital Appointment Operations Analysis
