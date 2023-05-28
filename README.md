## Calambug Dating Web App
The dating website project developed on Django is a powerful and reliable tool for people who are looking for their significant other. The website provides a high degree of personalization, security, and performance, making it an ideal choice for anyone who wants to find love online.

## About The Project

|  | Notes |
|--|--|
| ✅ | Registration / Authorization / Authentication |
| ✅ | Personalization (profile pic, cover and personal information) |
| ✅ | Chat between users |
| ✅ | Search (with filter) |
| ✅ | Internationalization and localization I18N |
| ✅ | Recommendation for dating |
| ✅ | Adding to Favorites |


### Built With
- ![Python](https://img.shields.io/badge/Python%20-%2314354C.svg?style=for-the-badge&logo=python&logoColor=white)
- ![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=green)
- ![SQLite](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white)
- ![Bootstrap](https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white)
- ![Docker](https://img.shields.io/badge/Docker-2CA5E0?style=for-the-badge&logo=docker&logoColor=white)
## Getting Started
Clone repository

    git clone https://github.com/towiron/dating-web-app.git

### Start with docker

1.Go into the repository

    cd dating-web-app

2.Build Docker image

    docker build -t dating

3.Run Docker image

    docker run --name dating_web_app -p 8000:8000 -d dating

4.Open the browser and go to http://localhost:8000/

### Start locally
1.Go to the repository

    cd dating-web-app

2.Create Python virtual environment

    python3 -m venv venv

 3.Activate a Python virtual environment and install dependencies:
> (MacOS/Unix)

     source venv/bin/activate
     pip3 install -r req.txt
> (Windows)

    venv\Scripts\activate.bat
    pip3 install -r req.txt

 4.For first time you need to create a SQLite database, by running the command
 

    python3 manage.py migrate

 
5.Run the server

    python3 manage.py runserver

 6.Open the browser and go to http://localhost:8000/
