# Fastapi MongoDB REST API


Setup env
```
virtualenv venv
```
For Linux/Mac
```
source venv/bin/activate
```
For Windows
```
source venv/Scripts/activate
```
Install package
```
pip install fastapi pymongo uvicorn
```
Start server 
```
uvicorn index:app --reload
```
![Fastapi-mongodb](https://user-images.githubusercontent.com/16520789/118378578-6ec43e80-b5f2-11eb-99bb-1a28abe9b5ed.png)



when new changes are made to the app build using
```
docker build -t fastapi-mongodb-restapi .
```

to run the app use the following commands
```
docker run -d -p 8000:8000 fastapi-mongodb-restapi
```

A postman documentation of the api, can be found here.
https://documenter.getpostman.com/view/9702163/2s9Y5R3mz9

