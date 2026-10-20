### 2.1. C4 Container Diagram

C4Context
    title System Context Diagram for AutoSpark Pro

    Person(owner, "Власник авто", "B2C-користувач, ініціює діагностику")
    Person(master, "Майстер СТО", "B2B-користувач, керує пулом авто")
    Person(admin, "Адміністратор", "Керує довідниками DTC")

    System(autoSpark, "AutoSpark Pro", "Екосистема діагностики авто")

    System_Ext(obdAdapter, "OBD-II Адаптер (ELM327)", "Bluetooth-адаптер")
    System_Ext(telegramApi, "Telegram API", "Зовнішній сервіс для бота")

    Rel(owner, autoSpark, "Зчитує діагностику, переглядає історію", "HTTPS / REST")
    Rel(master, autoSpark, "Розширена діагностика, генерація звітів", "HTTPS / REST")
    Rel(admin, autoSpark, "Керує DTC-базою", "HTTPS / REST")
    Rel(autoSpark, obdAdapter, "Зчитує телеметрію", "Bluetooth (AT-команди)")
    Rel(autoSpark, telegramApi, "Надсилає повідомлення", "HTTPS / Telegram Bot API")
