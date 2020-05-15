# Upgrade Django from 1.9 to 2.1

## In command prompt

1. cd into the folder you want to work in.

2. Make Virtual Environment
```console
pip freeze

pip install virtualenv
virtualenv mysiteENV
```


3. Activate Eneviornment
```console
mysiteENV\scripts\activate.dat
```

4. Install Django
```console
pip install django 
```

then install the databse client for Postgres

```console
pip install psycopg2 or

pip install --only-binary :all: mysqlclient
```

or whatever database package you're using.

5.Make sure Django is installed


```console
python -m django --version
``` 