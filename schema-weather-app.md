```mermaid
graph LR
    subgraph ВХОД
        A[main.py<br/>точка входа]
    end

    subgraph КОНФИГУРАЦИЯ
        B[Загрузка .env<br/>load_dotenv]
        C[Config<br/>чтение переменных]
        D{Валидация<br/>LATITUDE, LONGITUDE,<br/>START_DATE, END_DATE,<br/>HOURLY, TIMEZONE}
        E[AppConfig<br/>dataclass]
    end

    subgraph EXTRACT
        F[Extractor<br/>get_params]
        G[Retry механизм<br/>5 попыток]
        H[HTTP GET<br/>Open-Meteo API]
    end

    subgraph TRANSFORM_LOAD
        I[JSON ответ]
        J[Transform<br/>dict_to_df]
        K[pandas<br/>DataFrame]
        L{OUTPUT_FORMAT?}
        M[Сохранить CSV<br/>to_csv]
        N[Сохранить Parquet<br/>to_parquet]
    end

    subgraph РЕЗУЛЬТАТ
        O[(data/<br/>weather_start_to_end.csv)]
        P[(data/<br/>weather_start_to_end.parquet)]
        Q[(logfiles/<br/>app.log)]
    end

    A --> B --> C --> D
    D -->|ошибка| R[raise ValueError]
    D -->|успех| E --> F --> G --> H
    
    H --> I --> J --> K --> L
    L -->|csv| M --> O
    L -->|parquet| N --> P
    
    K -.-> S[Логирование]
    M -.-> S
    N -.-> S
    S -.-> Q
    
    G -.->|экспоненциальная<br/>задержка| G
    H -.->|сетевая ошибка| G

    classDef default fill:#f9f9f9,stroke:#333,stroke-width:2px,color:#000
    classDef start fill:#c8e6c9,stroke:#2e7d32,stroke-width:2px,color:#000
    classDef error fill:#ffcdd2,stroke:#c62828,stroke-width:2px,color:#000
    classDef api fill:#fff3e0,stroke:#e65100,stroke-width:2px,color:#000
    classDef dataframe fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px,color:#000
    classDef data fill:#e1f5fe,stroke:#01579b,stroke-width:2px,color:#000
    classDef log fill:#f3e5f5,stroke:#4a148c,stroke-width:2px,color:#000

    class A start
    class R error
    class H api
    class K dataframe
    class O,P data
    class Q log
```
