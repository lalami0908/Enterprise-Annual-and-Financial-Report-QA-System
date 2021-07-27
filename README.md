# Enterprise-Annual-and-Financial-Report-QA-System

## Usage
Since the file size is too large, the directory is missing
```
- 1. /bertmodels
- 2. /jsons
```
Please contact me if necessary

### server:
```
$ cd server
$ virtualenv env
$ source env/bin/activate  
$ pip3 install -r requirements.txt
$ python3 server.py 
```

### client:
```
$ npm run serve
```
it will run on http://localhost:8080/

### Third-party packages and frameworks used:

- Frontend: VueJs
- Backend: Python3, Flask
- Packages: transformers, sentence-transformers, torch, flask_sqlalchemy and so on (See more in the requirements.txt)
