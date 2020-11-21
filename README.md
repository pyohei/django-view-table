# django-view-table

Plugin to create view table in Django.  
This plugin enable you to create view table in Django model.  

## Support Database

* SQLite3
* PostgreSQL
* (TBC)MySQL
* (TBC)Oracle Database

## Installation & Setup

```
pip install django-view-table
```

After install, you can set your `INSTALLED_APPS`

```python
INSTALLED_APPS = [
    'viewtable',
]
```

## Usage

As Django app, you can create tables the below command.  

```bash
python manage.py createviewtable
```

This command works as follows. 

* Drop table
* Create table

So, first of all, you need to migrate your model.  


## License

MIT
