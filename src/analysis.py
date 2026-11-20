"""Project 9: Hospital Appointment Operations Analysis.

Run from the project root: python src/analysis.py

Install: pip install pandas numpy matplotlib seaborn

"""


# ------------------------------------------------------------------------------

# Import required libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

pd.set_option("display.max_columns", None)
pd.set_option("display.width", 140)
sns.set_theme(style="whitegrid")

# Read the CSV file. This path works when the notebook is run from the project root.
DATA_PATH = Path("data/09_hospital_appointments_100_records.csv")
if not DATA_PATH.exists():
    # Also allow running the notebook from the src folder.
    DATA_PATH = Path("../data/09_hospital_appointments_100_records.csv")

appointments = pd.read_csv(DATA_PATH)
appointments["Appointment_Date"] = pd.to_datetime(appointments["Appointment_Date"])

print("Dataset loaded successfully.")
print("Shape:", appointments.shape)



# ------------------------------------------------------------------------------

display(appointments.head())
print("\nDataset information:")
appointments.info()
print("\nDescriptive statistics:")
display(appointments.describe(include="all").T)
print("\nColumn names:", appointments.columns.tolist())



# ------------------------------------------------------------------------------

print("Missing values by column:")
display(appointments.isna().sum().to_frame("Missing_Count"))

# Preserve a flag before imputing attended appointment values.
appointments["Waiting_Time_Imputed"] = False
attended_missing = (
    appointments["Attendance_Status"].eq("Attended")
    & appointments["Waiting_Time_Minutes"].isna()
)
appointments.loc[attended_missing, "Waiting_Time_Imputed"] = True

# Missing waiting times for non-attended appointments are not applicable.
not_attended_missing = (
    appointments["Attendance_Status"].ne("Attended")
    & appointments["Waiting_Time_Minutes"].isna()
)
print("Missing waiting times for attended appointments:", int(attended_missing.sum()))
print("Missing waiting times for non-attended appointments (left as N/A):", int(not_attended_missing.sum()))

# Impute only attended records, using their department median.
department_medians = appointments.loc[
    appointments["Attendance_Status"].eq("Attended")
].groupby("Department")["Waiting_Time_Minutes"].median()

for department, median_value in department_medians.items():
    mask = (
        appointments["Department"].eq(department)
        & appointments["Attendance_Status"].eq("Attended")
        & appointments["Waiting_Time_Minutes"].isna()
    )
    appointments.loc[mask, "Waiting_Time_Minutes"] = median_value

print("\nMissing values after handling:")
display(appointments.isna().sum().to_frame("Remaining_Missing"))



# ------------------------------------------------------------------------------

duplicate_mask = appointments["Appointment_ID"].duplicated(keep="first")
duplicate_records = appointments.loc[duplicate_mask]
print("Duplicate Appointment_ID rows:", int(duplicate_mask.sum()))
display(duplicate_records)

# Retain the first occurrence of each appointment ID for all subsequent appointment-level analysis.
appointments = appointments.drop_duplicates(subset="Appointment_ID", keep="first").copy()
print("Records after duplicate removal:", len(appointments))
print("Remaining duplicate IDs:", int(appointments["Appointment_ID"].duplicated().sum()))



# ------------------------------------------------------------------------------

total_appointments = len(appointments)
attendance_counts = appointments["Attendance_Status"].value_counts()
attendance_percentages = (
    appointments["Attendance_Status"].value_counts(normalize=True).mul(100).round(2)
)
attendance_summary = pd.DataFrame({
    "Appointment_Count": attendance_counts,
    "Percentage": attendance_percentages
})
print("Total appointments:", total_appointments)
display(attendance_summary)



# ------------------------------------------------------------------------------

attended = appointments.loc[appointments["Attendance_Status"].eq("Attended")].copy()
department_waiting_summary = (
    attended.groupby("Department")
    .agg(
        Attended_Appointments=("Appointment_ID", "count"),
        Average_Wait_Minutes=("Waiting_Time_Minutes", "mean"),
        Median_Wait_Minutes=("Waiting_Time_Minutes", "median"),
        Maximum_Wait_Minutes=("Waiting_Time_Minutes", "max")
    )
    .round(2)
    .sort_values("Average_Wait_Minutes", ascending=False)
)
display(department_waiting_summary)



# ------------------------------------------------------------------------------

department_attendance = pd.crosstab(
    appointments["Department"],
    appointments["Attendance_Status"]
)
department_attendance["Total_Appointments"] = department_attendance.sum(axis=1)
department_attendance["No_Show_Percentage"] = (
    department_attendance.get("No-show", 0) / department_attendance["Total_Appointments"] * 100
)
department_attendance = department_attendance.sort_values(
    "No_Show_Percentage", ascending=False
).round(2)
display(department_attendance)
print("\nDepartment with highest no-show percentage:",
      department_attendance["No_Show_Percentage"].idxmax())



# ------------------------------------------------------------------------------

sms_attendance_counts = pd.crosstab(
    appointments["SMS_Reminder"], appointments["Attendance_Status"]
)
sms_attendance_percentages = pd.crosstab(
    appointments["SMS_Reminder"],
    appointments["Attendance_Status"],
    normalize="index"
).mul(100).round(2)
print("Counts:")
display(sms_attendance_counts)
print("Row percentages:")
display(sms_attendance_percentages)

no_show_rates = (
    appointments.assign(Is_No_Show=appointments["Attendance_Status"].eq("No-show"))
    .groupby("SMS_Reminder")["Is_No_Show"].mean().mul(100).round(2)
)
print("No-show percentage by SMS reminder:")
display(no_show_rates.to_frame("No_Show_Percentage"))



# ------------------------------------------------------------------------------

department_fee_summary = (
    appointments.groupby("Department")
    .agg(
        Appointment_Count=("Appointment_ID", "count"),
        Average_Consultation_Fee=("Consultation_Fee", "mean"),
        Median_Consultation_Fee=("Consultation_Fee", "median")
    )
    .round(2)
    .sort_values("Average_Consultation_Fee", ascending=False)
)
display(department_fee_summary)



# ------------------------------------------------------------------------------

daily_department_volume = pd.pivot_table(
    appointments,
    index="Appointment_Date",
    columns="Department",
    values="Appointment_ID",
    aggfunc="count",
    fill_value=0
).sort_index()
display(daily_department_volume.head(15))
print("Total appointment volume represented in date-department table:",
      int(daily_department_volume.to_numpy().sum()))

daily_total = appointments.groupby("Appointment_Date").size()
plt.figure(figsize=(12, 4))
daily_total.plot(kind="line", marker="o")
plt.title("Daily Appointment Volume")
plt.xlabel("Appointment Date")
plt.ylabel("Number of Appointments")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()



# ------------------------------------------------------------------------------

appointment_type_wait = (
    attended.groupby("Appointment_Type")["Waiting_Time_Minutes"]
    .agg(["count", "mean", "median", "min", "max"])
    .round(2)
)
display(appointment_type_wait)

plt.figure(figsize=(7, 4))
sns.boxplot(data=attended, x="Appointment_Type", y="Waiting_Time_Minutes")
plt.title("Waiting Time: New vs Follow-up Appointments")
plt.xlabel("Appointment Type")
plt.ylabel("Waiting Time (minutes)")
plt.tight_layout()
plt.show()



# ------------------------------------------------------------------------------

waiting_array = attended["Waiting_Time_Minutes"].dropna().to_numpy(dtype=float)

waiting_median = np.median(waiting_array)
q1, q2, q3 = np.percentile(waiting_array, [25, 50, 75])
waiting_std_population = np.std(waiting_array, ddof=0)
waiting_std_sample = np.std(waiting_array, ddof=1)

print(f"Number of attended appointments with waiting-time values: {len(waiting_array)}")
print(f"Median: {waiting_median:.2f} minutes")
print(f"Q1 (25th percentile): {q1:.2f} minutes")
print(f"Q2 (50th percentile): {q2:.2f} minutes")
print(f"Q3 (75th percentile): {q3:.2f} minutes")
print(f"Population standard deviation: {waiting_std_population:.2f} minutes")
print(f"Sample standard deviation: {waiting_std_sample:.2f} minutes")



# ------------------------------------------------------------------------------

iqr = q3 - q1
lower_bound = q1 - 1.5 * iqr
upper_bound = q3 + 1.5 * iqr

waiting_outliers = attended.loc[
    (attended["Waiting_Time_Minutes"] < lower_bound)
    | (attended["Waiting_Time_Minutes"] > upper_bound),
    ["Appointment_ID", "Appointment_Date", "Department",
     "Appointment_Type", "Waiting_Time_Minutes"]
].sort_values("Waiting_Time_Minutes", ascending=False)

print(f"IQR: {iqr:.2f}")
print(f"Lower fence: {lower_bound:.2f} minutes")
print(f"Upper fence: {upper_bound:.2f} minutes")
print("Potential waiting-time outliers:", len(waiting_outliers))
display(waiting_outliers)



# ------------------------------------------------------------------------------

# Categories are operational bands chosen for this teaching analysis.
# They are not medical or regulatory thresholds.
bins = [-np.inf, 15, 30, 60, np.inf]
labels = ["0-15 minutes", "16-30 minutes", "31-60 minutes", "Above 60 minutes"]

attended["Waiting_Time_Category"] = pd.cut(
    attended["Waiting_Time_Minutes"],
    bins=bins,
    labels=labels,
    right=True
)
waiting_band_summary = (
    attended["Waiting_Time_Category"]
    .value_counts(sort=False)
    .rename_axis("Waiting_Time_Category")
    .to_frame("Appointment_Count")
)
waiting_band_summary["Percentage"] = (
    waiting_band_summary["Appointment_Count"] / waiting_band_summary["Appointment_Count"].sum() * 100
).round(2)
display(waiting_band_summary)

plt.figure(figsize=(8, 4))
waiting_band_summary["Appointment_Count"].plot(kind="bar")
plt.title("Attended Appointments by Waiting-Time Category")
plt.xlabel("Waiting-Time Category")
plt.ylabel("Number of Appointments")
plt.xticks(rotation=15)
plt.tight_layout()
plt.show()



# ------------------------------------------------------------------------------

attended_fee_summary = (
    attended.groupby("Department")
    .agg(
        Attended_Appointments=("Appointment_ID", "count"),
        Estimated_Attended_Fees=("Consultation_Fee", "sum"),
        Average_Fee=("Consultation_Fee", "mean")
    )
    .sort_values("Estimated_Attended_Fees", ascending=False)
)
display(attended_fee_summary)
estimated_total_attended_fees = attended["Consultation_Fee"].sum()
print(f"Estimated total consultation fees for attended appointments: ₹{estimated_total_attended_fees:,.2f}")
print("Assumption: each attended appointment's listed consultation fee is treated as collected/earned.")



# ------------------------------------------------------------------------------

# Recommendations are generated from the observed sample metrics.
highest_noshow_dept = department_attendance["No_Show_Percentage"].idxmax()
highest_noshow_rate = department_attendance.loc[highest_noshow_dept, "No_Show_Percentage"]

sms_rates = no_show_rates.to_dict()
if "Yes" in sms_rates and "No" in sms_rates:
    sms_direction = (
        "The observed no-show rate is lower for appointments with SMS reminders."
        if sms_rates["Yes"] < sms_rates["No"]
        else "The observed no-show rate is not lower for appointments with SMS reminders."
    )
else:
    sms_direction = "The sample does not contain both SMS reminder groups."

busiest_date = daily_total.idxmax()
busiest_count = int(daily_total.max())
long_wait_dept = department_waiting_summary["Average_Wait_Minutes"].idxmax()
long_wait_avg = department_waiting_summary.loc[long_wait_dept, "Average_Wait_Minutes"]
outlier_count = len(waiting_outliers)

recommendations = [
    f"Review appointment confirmation and rescheduling processes in {highest_noshow_dept}, which has the highest observed no-show percentage ({highest_noshow_rate:.1f}%).",
    f"Evaluate the SMS reminder workflow. {sms_direction} In this dataset, the no-show rates are {sms_rates.get('Yes', np.nan):.1f}% for Yes and {sms_rates.get('No', np.nan):.1f}% for No; this is an association, not proof that reminders cause the difference.",
    f"Review staffing and appointment-slot allocation around {busiest_date.date()}, the busiest date in the sample ({busiest_count} appointments).",
    f"Audit scheduling and queue processes in {long_wait_dept}, which has the highest department average waiting time ({long_wait_avg:.1f} minutes). Consider appointment spacing and workload balancing.",
    f"Review the {outlier_count} potential unusually long waiting-time records individually and monitor waiting-time bands regularly; IQR flags unusual values but does not establish the reason for a delay."
]

for number, recommendation in enumerate(recommendations, start=1):
    print(f"{number}. {recommendation}")
