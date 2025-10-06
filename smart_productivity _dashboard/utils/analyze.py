def get_summary(df, employee_name):
    emp_df = df[df['Name'] == employee_name]
    summary = {
        "Total Days": emp_df.shape[0],
        "Total Hours Worked": emp_df['HoursWorked'].sum(),
        "Total Tasks Completed": emp_df['TasksCompleted'].sum(),
        "Days Present": emp_df[emp_df['Attendance'] == 'Present'].shape[0],
        "Avg Hours/Day": round(emp_df['HoursWorked'].mean(), 2),
        "Avg Tasks/Day": round(emp_df['TasksCompleted'].mean(), 2),
    }
    return summary
