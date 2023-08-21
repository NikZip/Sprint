<p align="center">
      <img src="https://lms-cdn.skillfactory.ru/assets/courseware/v1/6ce6d0d69d2954ea1ef1511b7c4c6fca/asset-v1:SkillFactory+PDEV+2021+type@asset+block/virt_intern_start_2.1.svg" width="250">
</p>

<p align="center">
   <img src="https://img.shields.io/badge/App_Version-v1.0-w" alt="App Version">
  <img src="https://img.shields.io/badge/Django-v4.2.3-w" alt="Django Version">
   <img src="https://img.shields.io/badge/License-MIT-brightgreen" alt="License">
</p>

# About
This is REST API for mobile application that FSTR commissioned SkillFactory students to develop that would make it easier for tourists to submit pass data and reduce the request processing time to three days.

# Install

1. Clone the repository or download the zip file
```
git clone https://github.com/NikZip/Sprint
```
2. Rename file **`.env_template`** to **`.env`** and full **`DATABASE DATA`**  with yours

3. Install dependencies
```
pip install -r requirements.txt
```
4. Run migrations
```
python manage.py makemigrations
```

```
python manage.py migrate
```
5. Run tests
```
pytest
```

# Endpoints:
### POST **`api/v1/perivals`**
### GET/PATCH **`api/v1/perivals/id`**
### GET **`api/v1/perivals/search/?user__email`**

# [Swagger API Documentation](https://app.swaggerhub.com/apis/NIKZIPDEV_1/RESTAPI-Docs-FSTRapp/v1)
### In app docs url **`api/v1/docs/`**

