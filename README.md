
# **PackTime Scheduling and Job Management Application

### **Overview**

The **PackTime Scheduling and Job Management Application** is a comprehensive tool designed for **job scheduling**, **real-time collaboration**, and **advanced reporting** in a manufacturing or production environment. The app helps operators and managers streamline the scheduling process, manage jobs efficiently, and track machine and operator performance. It also includes real-time notifications, job dependency management, and automated reports to enhance operational efficiency.

---

### **Key Features**

1. **Real-Time Job Scheduling and Management**:
   - **Job creation, assignment, and editing** with real-time updates.
   - **Automatic scheduling suggestions** based on machine availability and operator schedules.
   - **Real-time collaboration** via chat and task comments for jobs.

2. **Advanced Reporting and Forecasting**:
   - **Job forecasting** with predicted completion times and machine load predictions.
   - **Dynamic reporting** for job statuses, machine performance, and operator workloads.
   - **Customizable report generation** with PDF and CSV export options.

3. **Notifications and Alerts**:
   - **Real-time notifications** for job updates, changes in schedules, and task assignments.
   - **Customizable alert settings**: Users can choose to receive notifications about job statuses, conflicts, and reminders.
   - **Live activity feed** to track job progress and updates.

4. **Job Dependency and Conflict Management**:
   - Manage **job dependencies** and track conflicts in real-time.
   - **Automatic conflict detection** and alerts for overlapping jobs or unmet dependencies.

5. **Multi-User Collaboration**:
   - **Role-based views and access** for managers and operators.
   - **Collaborative job editing** without overwriting changes.
   - **Task-specific chat** to discuss job details and issues.

6. **Mobile-Friendly and Accessible**:
   - **Mobile-responsive design** for seamless use on tablets and smartphones.
   - **Accessibility enhancements** for screen readers, keyboard navigation, and contrast adjustments.

---

### **Technologies Used**

- **Streamlit**: For building the interactive web app.
- **Pandas**: For handling job data and generating reports.
- **NetworkX**: For creating and visualizing job dependency graphs.
- **Matplotlib**: For data visualizations and reporting charts.
- **FPDF**: For generating job traveler PDFs.
- **GitHub**: For code version control and deployment.


---

### **Setup Instructions**

1. **Install Python Dependencies**:
   To run the application locally, you need Python and several libraries. First, ensure you have **Python 3.7+** installed.

   Then, install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configuration**:
   The application uses **Streamlit's session state** to store user preferences and job data. Ensure that you have the required environment variables set up or use the default values in the code.

3. **Run the Application**:
   To launch the app locally, navigate to the project directory and run:
   ```bash
   streamlit run app.py
   ```

---

### **Customizing the Application**

You can customize the following parts of the app to fit your specific needs:

1. **User Roles**: Update the role management section to fit your organization’s hierarchy (e.g., manager, operator, etc.).
2. **Job Data**: Modify the job creation and management sections to include fields relevant to your production or manufacturing environment.
3. **Report Templates**: Modify the PDF or CSV report generation to reflect specific metrics and KPIs relevant to your operations.
4. **Branding**: Update the app’s color scheme, logo, and theme to match your company’s branding.

---

### **FAQ**

**Q: Can I add more machines or operators to the system?**

A: Yes, you can modify the job data structure to include more machines or operators. The app uses Pandas DataFrames, so you can easily add rows to reflect new machines or users.

**Q: How do I export reports?**

A: The app allows you to generate **CSV** and **PDF** reports for jobs, performance, and forecasts. Simply select the data you want to export and click the "Download" button.

---

### **Contributors**

- **[Alden Spooner]**: Lead Developer & Project Manager
- **[Alden Spooner]**: Frontend Developer
- **[Alden Spooner]**: Data Scientist (for job scheduling and forecasting logic)

---

### **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
