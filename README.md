# vocabulary-api
Python service to provide vocabulary api


#### Run project :
1 - clone project :
```bash
$ git clone .......
```
2 - navigate to project-path/src/ :
```bash
$ cd project-path/src/
```
3 - install requirements :
```bash
$ pip install -r requirements.txt
```
4 - create database and migrate models :
```bash
$ python manage.py migrate
```
5 - insert prepared 20 words into database :
```bash
$ python manage.py loaddata fixtures.json
```
6 - run project :
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