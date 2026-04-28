# beyza-resume-app
# Interactive Resume Portal
**Full-Stack Developer Project**

## Executive Summary
This project is a dynamic, cloud-deployed professional resume. Unlike a static PDF, this portal allows for real-time content updates through an authenticated Admin panel and generates a customized PDF for recruiters on demand.

## The Tech Stack
* **Streamlit:** The primary framework for building the web interface.
* **Pandas:** Used for structured data handling.
* **FPDF:** For generating the downloadable PDF resume.
* **Pillow (PIL):** To handle profile picture processing and editing.
* **JSON:** Used as a lightweight database to store resume content.

## Agile Methodology
I managed this project using an **8-day sprint**. I utilized **Daily Standups** to track progress and identify blockers. This allowed me to prioritize the "Resume View" as my Minimum Viable Product (MVP) before moving on to the "Admin Photo Editor" and PDF generation features.

## Technical Milestones
* **CRUD Operations:** The app can **Create/Update** resume data via the Admin sidebar, **Read** data from `resume_data.json`, and **Delete/Overwrite** images in the local storage.
* **Virtual Environment:** I used a `.venv` to ensure that all dependencies were isolated and consistent.
* **Deployment:** The app is deployed via **Streamlit Cloud**, synced directly with this GitHub repository for continuous deployment.

## AI Collaboration
I worked with AI as a "Senior Engineer" partner. I used it primarily to troubleshoot PDF encoding issues with `latin-1` and to optimize the logic that toggles between "Guest View" and "Admin View" using session states.
