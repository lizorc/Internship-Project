# Internship-project


|Project Name|Developer| Date
-------------| ---------|---
|Follow-up on the expansion of the STN and STR|Liz Oriana Rodrigues C.| 2022|

## Introduction 
Intuitive and facilitating application to perform the process of monitoring the expansion of the STR and STN in an automated way to calculate which projects should be charged and the corresponding value depending on the month. 

## Installation
Initially you will need the following programs and libraries installed. 
1.	[Python](https://www.python.org/downloads/)
    - [FastAPI](https://pypi.org/project/fastapi/)
    - [SQLAlchemy](https://pypi.org/project/SQLAlchemy/)
    - [uvicorn](https://pypi.org/project/uvicorn/)
    - [pydantic](https://pypi.org/project/pydantic/)
    - [starlette](https://pypi.org/project/starlette/)
    - [DateTime](https://pypi.org/project/DateTime/)
2.	[Visual Studio Code](https://code.visualstudio.com/Download)
3.	[SQLite](https://www.sqlite.org/download.html)

## Structure
Currently the structure is as follows.

```
| backend
|
├── models
|    ├── AGE_model.py
|    ├── AMP_STN_model.py
|    ├── AMP_STR_model.py
|    ├── CON_STN_model.py
|    ├── CON_STR_model.py
|    ├── DA_AMP_model.py
|    ├── LIQ_model.py
|    ├── PRO_model.py
|    └── SE_FPO_model.py
|    
├── schemas
|    ├── AGE_schema.py
|    ├── AMP_STN_schema.py
|    ├── AMP_STR_schema.py
|    ├── CON_STN_schema.py
|    ├── CON_STR_schema.py
|    ├── DA_AMP_schema.py
|    ├── LIQ_schema.py
|    ├── PRO_schema.py
|    └── SE_FPO_schema.py
|    
├── CRUD
|    ├── AGE_crud.py
|    ├── AMP_STN_crud.py
|    ├── AMP_STR_crud.py
|    ├── CON_STN_crud.py
|    ├── CON_STR_crud.py
|    ├── DA_AMP_crud.py
|    ├── LIQ_crud.py
|    ├── PRO_crud.py
|    └── SE_FPO_crud.py
|    
├── validations
|    ├── AGE_validation.py
|    ├── AMP_STN_validation.py
|    ├── AMP_STR_validation.py
|    ├── CON_STN_validation.py
|    ├── CON_STR_validation.py
|    ├── DA_AMP_validation.py
|    ├── GENERAL_validation.py
|    ├── LIQ_validation.py
|    ├── PRO_validation.py
|    └── SE_FPO_validation.py
|    
├── request
|    ├── API_connection.py
|    └── API_extraction.py
|    
├── __init__.py
├── database.py
└── main.py
```

```
| db
├── Data.db 
```


## Test
- Run the server from the terminal.

    ```python
    uvicorn backend.main:app --reload
    ```

    - The following response will appear.

        ```python
        INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)

        INFO:     Started reloader process [28720] 

        INFO:     Started server process [28722]

        INFO:     Waiting for application startup. 

        INFO:     Application startup complete. 
        ```

***NOTE**: This means that the server is running correctly.*

