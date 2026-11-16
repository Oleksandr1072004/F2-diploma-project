Software Requirements Specification (SRS)

**Проєкт:** AutoSpark Pro

**Стандарт:** ISO/IEC/IEEE 29148

## **1. System Context (Контекст системи)**

Система AutoSpark Pro є розподіленою клієнт-серверною екосистемою для автомобільної діагностики. Межі системи охоплюють мобільний клієнт (Flutter), серверні сервіси (FastAPI), брокер повідомлень (Apache Kafka), бази даних (PostgreSQL, Redis) та Telegram-бот (aiogram). Система взаємодіє із зовнішніми сутностями: OBD-II адаптер (ELM327) через Bluetooth, Telegram API (зовнішній сервіс) та користувачами (власник авто, майстер СТО). Система не включає розробку власного апаратного забезпечення OBD-II, а використовує стандартні адаптери.

## **2. Functional Requirements (Функціональні вимоги)**

| **ID** | **Вимога** | **Модуль** |
| --- | --- | --- |
| **SRS-FUN-01** | Система повинна зчитувати параметри OBD-II (RPM, швидкість, температура, напруга) через Bluetooth із частотою дискретизації ≥ 10 Гц. | Мобільний клієнт |
| **SRS-FUN-02** | Система повинна виконувати декодування DTC-кодів із прив'язкою до внутрішньої бази знань та зберігати результати в PostgreSQL. | Backend |
| **SRS-FUN-03** | Система повинна публікувати події діагностики в Apache Kafka для асинхронної обробки фоновими сервісами. | Message Broker |
| **SRS-FUN-04** | Система повинна надавати автентифікацію користувачів через OAuth 2.0 / OIDC із використанням підписаних JWT-токенів. | Auth Service |
| **SRS-FUN-05** | Система повинна генерувати PDF-звіти з агрегованою історією діагностик для кожного автомобіля. | Report Service |
| **SRS-FUN-06** | Система повинна надавати користувачу доступ до історії діагностик та розшифровки DTC-кодів через Telegram-бот. | Telegram Bot |
| **SRS-FUN-07** | Система повинна відображати динамічні графіки параметрів у реальному часі на клієнті Flutter. | Мобільний клієнт |
| **SRS-FUN-08** | Система повинна експортувати метрики до Prometheus та трейси до Jaeger через OpenTelemetry. | Infrastructure |

## **3. Non-Functional Requirements (NFRs Matrix)**

| **ID** | **Категорія** | **Вимога** |
| --- | --- | --- |
| **SRS-NFR-PERF-01** | Продуктивність | Latency API на p95 ≤ 200 мс при навантаженні 500 RPS. |
| **SRS-NFR-SCALE-01** | Масштабованість | Горизонтальне масштабування FastAPI-сервісів до 10 інстансів через Docker/Kubernetes. |
| **SRS-NFR-ASYNC-01** | Асинхронність | Apache Kafka повинен обробляти ≥ 1000 подій/с. |
| **SRS-NFR-SEC-01** | Безпека | Автентифікація OAuth 2.0 / OIDC, підписані JWT-токени, TLS 1.3. |
| **SRS-NFR-SEC-02** | Комплаєнс | Відповідність GDPR (право на видалення), OWASP ASVS Level 2. |
| **SRS-NFR-RELI-01** | Надійність | Circuit Breaker, Retry with Exponential Backoff, доступність 99.5%. |
| **SRS-NFR-OBS-01** | Спостережуваність | OpenTelemetry, Prometheus, Grafana, Jaeger. |
| **SRS-NFR-BACKUP-01** | Резервне копіювання | Щоденний бекап PostgreSQL: RPO ≤ 1 год, RTO ≤ 4 год. |

## **4. Verification Criteria (Критерії верифікації)**

| **ID вимоги** | **Метод верифікації** | **Інструмент** |
| --- | --- | --- |
| **SRS-FUN-01** | Інтеграційний тест із симуляцією OBD-II адаптера | pytest + ELM327 Emulator |
| **SRS-FUN-02** | Модульний тест декодування DTC | pytest |
| **SRS-FUN-03** | Тест асинхронної публікації в Kafka | pytest + Kafka Testcontainers |
| **SRS-FUN-04** | Тест автентифікації JWT | pytest + Postman |
| **SRS-FUN-05** | Тест генерації PDF | pytest + WeasyPrint |
| **SRS-NFR-PERF-01** | Стрес-тест (Spike Testing) | k6 |
| **SRS-NFR-SEC-01** | Статичний аналіз коду | SonarQube + Trivy |
| **SRS-NFR-SEC-02** | Аудит залежностей | Trivy + Dependabot |
| **SRS-NFR-RELI-01** | Chaos Engineering тест | Testcontainers + Toxiproxy |
| **SRS-NFR-OBS-01** | Перевірка експорту метрик | Prometheus + Grafana |

## **5. Glossary (Глосарій)**

| **Термін** | **Визначення** |
| --- | --- |
| **OBD-II** | On-Board Diagnostics II — стандарт діагностики автомобіля (SAE J1962). |
| **DTC** | Diagnostic Trouble Code — код помилки, що ідентифікує несправність. |
| **EDA** | Event-Driven Architecture — архітектура, де компоненти взаємодіють через події. |
| **CQRS** | Command Query Responsibility Segregation — розділення операцій читання та запису. |
| **Saga** | Патерн управління розподіленими транзакціями через компенсуючі дії. |
| **Latency p95** | 95-й перцентиль часу відгуку системи. |
| **JWT** | JSON Web Token — підписаний токен для автентифікації. |
