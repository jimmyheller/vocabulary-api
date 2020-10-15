# vocabulary-api
Python service to provide vocabulary api

#### Docker :
1- clone project 
```bash
$ git clone .......
```
2- navigate to project root ( where the Docker file located):
```bash
$ cd project-path/
```
3- build image with this command ( it might take time ):
```bash
$ docker-compose up -d
```

#### Run project manually:
1- clone project :
```bash
$ git clone .......
```
2- navigate to project-path/src/ :
```bash
$ cd project-path/src/
```
3- install virtualenv :
```bash
$ pip install virtualenv
```
4- creating virtualenv :
```bash
$ virtualenv venv
```
5- active virtualenv :
```bash
$ source venv/bin/activate
```
6- install requirements :
```bash
$ pip install -r requirements.txt
```
7- create database and migrate models :
```bash
$ python manage.py migrate
```
8- insert prepared 20 words into database :
```bash
$ python manage.py loaddata fixtures.json
```
9- run project :
```bash
$ python manage.py runserver
```

### To test
to run test case about random-word :

1- run project :
```bash
$ python manage.py runserver
```
2- in another terminal :
```bash
$ python manage.py test vocab
```


### REST documentation
to view REST end-points after running the project , hit the browser into this address :
```bash
127.0.0.1:8000/docs
```