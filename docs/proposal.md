# Thesis Proposal: AutoSpark Pro

**Author:** Гриненко Олександр Васильович
**Supervisor:** Остапов Сергій Едуардович
**Specialty:** F2 Software Engineering

## Project Title
**UA:** Розробка екосистеми AutoSpark Pro для діагностики та обслуговування автомобілів.
**EN:** Development of the AutoSpark Pro Ecosystem for Vehicle Diagnostics and Maintenance.

## Relevance and Problem Statement
The modern automotive service market is characterized by the high cost of professional diagnostic equipment and its complexity for end-users. The primary problem is the lack of an accessible, integrated platform that combines a mobile application for reading sensor data, server-side analytics, and a convenient interface (e.g., a Telegram bot) for obtaining recommendations without expensive hardware.

## Product Idea
This project involves the development of a distributed client-server system consisting of three core components:
1.  **Mobile Client (Flutter):** For reading data from an OBD-II scanner via Bluetooth, providing real-time telemetry.
2.  **Backend Server (FastAPI):** For processing diagnostic data, managing users, and handling DTC databases.
3.  **Telegram Bot (aiogram):** For quick access to diagnostic history, DTC decoding, and AI-assisted FAQs.

## Core Features
1.  **OBD-II Data Reading:** Connection via Bluetooth to read RPM, speed, coolant temperature, and voltage.
2.  **DTC Management:** Reading, decoding, and clearing of engine fault codes.
3.  **Vehicle History:** Maintaining a service history log for each vehicle linked to a user profile.
4.  **Live Data Visualization:** Displaying dynamic graphs and gauges for real-time vehicle parameters.
5.  **Optical Inspection:** Photo capture for headlight condition analysis.
6.  **Automated Diagnosis (Telegram):** Decoding DTC codes sent by users to the bot.
7.  **PDF Report Generation:** Formulating a final diagnostic report for the client.

## Technology Stack
*   **Languages:** Dart (Flutter), Python (Backend/Bot).
*   **Frameworks:** FastAPI, aiogram, SQLAlchemy, Flutter SDK.
*   **Databases:** PostgreSQL, Redis.
*   **DevOps:** Docker, GitHub Actions, Git.
