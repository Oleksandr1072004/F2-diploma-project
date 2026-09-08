# Thesis Proposal: AutoSpark Pro

**Author:** Гриненко Олександр Васильович
**Supervisor:** Остапов Сергій Едуардович
**Specialty:** F2 Software Engineering

---

## Project Title
**UA:** Розробка розподіленої екосистеми AutoSpark Pro для діагностики та технічного обслуговування автомобілів.
**EN:** Development of the AutoSpark Pro Distributed Ecosystem for Vehicle Diagnostics and Maintenance.

---

## Relevance and Problem Statement
The modern automotive service market is characterized by the high cost of professional diagnostic equipment (e.g., VCDS, TechStream, Delphi) and its steep learning curve for non-professional users. Simultaneously, vehicle owners require rapid access to Diagnostic Trouble Code (DTC) decoding, real-time sensor data verification, and up-to-date maintenance information. The core problem is the absence of an accessible, integrated platform that combines a mobile application for data acquisition, server-side analytics, and a convenient interface (e.g., a Telegram bot) for obtaining actionable recommendations, thereby eliminating the need for expensive, stationary hardware.

---

## Product Idea
This project entails the development of a distributed client-server system comprising three core components:

1.  **Mobile Client (Flutter):** A cross-platform application for acquiring data from an automotive OBD-II scanner via Bluetooth, providing real-time telemetry, and performing basic diagnostic functions.
2.  **Backend Server (FastAPI):** A central backend responsible for processing diagnostic data, maintaining vehicle histories, managing user authentication and profiles, and interacting with DTC databases.
3.  **Telegram Bot (aiogram):** An assistant providing quick access to diagnostic history, decoding DTC codes, answering FAQs, and offering AI-driven consultations.

---

## Core Features
1.  **OBD-II Data Acquisition:** Establish a Bluetooth connection to read fundamental parameters (RPM, vehicle speed, coolant temperature, voltage) via the OBD-II protocol.
2.  **DTC Management:** Read, decode, and clear engine fault codes with reference to a built-in DTC database.
3.  **Vehicle History Management:** Maintain a detailed service history log, including diagnostics, mileage, recurring faults, and notes for each vehicle linked to a user profile (PostgreSQL).
4.  **Live Data Visualization:** Display dynamic graphs and gauges for real-time vehicle sensor data (e.g., oxygen sensor voltage, fuel pressure).
5.  **Headlight Optical Inspection:** Capture and upload photos for subsequent analysis of headlight condition and alignment verification.
6.  **Telegram-based Automated Diagnostics:** Users can send a DTC code to the bot, which returns a detailed description of the problem, probable causes, and estimated repair costs.
7.  **Automated PDF Report Generation:** Create a summary diagnostic report suitable for sharing with clients or archiving.

---

## Extended Engineering Scope (Proposed Enhancements)
To ensure architectural depth and enterprise-level resilience, the project will incorporate:
*   **Asynchronous Processing:** A message broker (RabbitMQ) will decouple the FastAPI application from long-running tasks (e.g., complex diagnostics, PDF generation), improving system responsiveness and fault tolerance.
*   **Database Scalability:** PostgreSQL Master-Slave replication will be implemented to separate read and write loads, ensuring performance under high traffic.
*   **DevSecOps Pipeline:** Static vulnerability scanning (e.g., Trivy) will be integrated into the GitHub Actions CI/CD pipeline to ensure container and code security.
*   **Application Monitoring:** An observability stack (Prometheus, Grafana) will be deployed to monitor system health, latency, and error rates of the backend and message queue.
*   **Resilience Patterns:** Client-side retry logic (with exponential backoff) and server-side circuit breakers will be implemented to handle transient failures gracefully.

---

## Preliminary Technology Stack
*   **Programming Languages:** Dart (Flutter), Python (Backend, Bot).
*   **Frameworks & Libraries:** Flutter SDK, FastAPI, aiogram, SQLAlchemy.
*   **Databases:** PostgreSQL (primary, with replication), Redis (caching, session management).
*   **Message Broker:** RabbitMQ (for asynchronous task queuing).
*   **DevOps & Infrastructure:** Docker (containerization), GitHub Actions (CI/CD), Git (version control).
*   **Monitoring & Security:** Prometheus, Grafana, Trivy.
