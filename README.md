## Favorite Things  App

## Description
The **favorite-things-app** is an application that allows the user to track and mannage their favorite things. The project is divided into two parts. The Frontend build on **VueJs - Javascript** and the Backend built on **Django(DRF) - Python**.


- Key Application features

2. Favorite Management
    - Creation of Favorites
    - Updating different Favorites
    - Removing different Favorites from the system
    - Filtering Favorites base on Category

2. Category Management
    - Creation of Categories
    - Updating different Categories
    - Removing different Categories from the system

- BackEnd

The api built using Django Rest framework deployed in AWS Lambda using Zappa provides resources, i.e. Collection of endpoints to track a user's favorite things.

- FrontEnd

The FrontEnd is a VueJs application located in the client folder deployed on netlify.

* Here is the [ LIVE FRONTEND URL](https://5d39aaf9a40c820009a38bd9--elegant-agnesi-f6c341.netlify.com/) of the application

I created  a test user to ease the process of testing the application
## Test User
* email - testuser@test.com
* password - password


## Technology Stack

- Django
- DRF
- Postgres(AWS RDS)
- ZAPPA(AWS LAMBDA)
- Docker
- VueJS


###  Setting Up For Local Development

-   Check that python 3 is installed:

    ```
    python --version
    >> Python 3.7.0
    ```

-   Install pipenv:

    ```
    brew install pipenv
    ```

-   Check pipenv is installed:
    ```
    pipenv --version
    >> pipenv, version 2018.10.13
    ```

-   Clone the favorite-thing repo and cd into it:

    ```
    git clone https://github.com/tonyguesswho/favorite-things.git
    ```

-   Install dependencies from requirements.txt file:

    ```
    pip install -r requirements.txt
    ```

-   Make a copy of the .env.sample file in the app folder and rename it to .env and update the variables accordingly:

    ```
    DJANGO_KEY=generate a random django key # https://www.miniwebtool.com/django-secret-key-generator/
    DB_NAME=dbname
    DB_USER=dbuser
    DB_PASSWORD=secretpassword

    ```

-   Activate a virtual environment:

    ```
    pipenv shell
    ```

-   Apply migrations:

    ```
    cd into the app folder and run python manage.py migrate
    ```

-   If you'd like to seed initial data to the database:

    ```
    Run python manage.py loaddata category.json to seed initial categories
    ```

*   Run the application with the command

    ```
    python manage.py runserver
    ```

*   Should you make changes to the database models, run migrations as follows

    -   make migration

        ```
        python manage.py makemigrations
        ```

    -   Migrate:
        ```
        python manage.py migrate
        ```

*   Deactivate the virtual environment once you're done:
    ```
    exit
    ```

## Running tests

On command line run:

```
python manage.py test
```


## Set Up Development With Docker

1. Download Docker from [here](https://docs.docker.com/)
2. Set up an account to download Docker
3. Install Docker after download
4. Go to your terminal run the command `docker login`
5. Input your Docker email and password

To setup for development with Docker after cloning the repository please do/run the following commands in the order stated below:

-   `cd <project dir>` to check into the dir
-   `docker-compose build`
-   `docker-compose up -d` to start the api after the previous command is successful

The `docker-compose build` command builds the docker image where the api and its postgres database would be situated.
Also this command does the necessary setup that is needed for the API to connect to the database.

The `docker-compose up -d` or `make start` command starts the application while ensuring that the postgres database is seeded before the api starts.


To stop the running containers run the command `docker-compose down`

## Local Deployment to AWS Lambda using Zappa

The API was deployed usind Zappa and the zappa_settings.json file is located in the app folder

-   Install zappa inside virtual environment:

    ```
    pip install zappa
    ```

-   Initialize project with zappa

    ```
    zappa init
    ```

-   Deploy project with zappa

    ```
    zappa deploy dev
    ```

-   Redeploy updates/changes with zappa

    ```
    zappa update dev
    ```

[LIVE HOMEPAGE](https://5d39aaf9a40c820009a38bd9--elegant-agnesi-f6c341.netlify.com "Homepage")

- Interact with backend API using the DRF template view
 https://8eiy0d8mpd.execute-api.us-east-1.amazonaws.com/dev/api/category/categories/



* Landing Page

![User Interface](https://user-images.githubusercontent.com/19865565/61905725-afd0f780-af21-11e9-9cf8-31e849c1f5db.png)


#### (Setting up the front end locally)
- Check that Node (recommended v11.12+) and npm are installed on your machine.

- Install dependencies
```
cd into the client folder and run npm install
```

- Create .env file in the client folder using the .env.example file as reference, add this to the .env
```
VUE_APP_API_URL=http://127.0.0.1:8000
```
- Run app
```
npm run serve
```
- Open Application in browser
```
http://127.0.0.1:8080
```
- Production build
```
npm run build
```

## Other Links

1. Link to the description of myself is [myself.json](https://github.com/tonyguesswho/favorite-things/blob/update-readme/myself.json)
2. Link to the answers to the remaining technical questions is [answers.md](https://github.com/tonyguesswho/favorite-things/blob/update-readme/answers.md)
3. Link to the debugging quiz is [quiz.py](https://github.com/tonyguesswho/favorite-things/blob/update-readme/quiz.py)


I will appreciate any feedback on this project :)