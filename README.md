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

### Create model

You need the three step.

* Import `view_table` module
* Inherit `ViewTable`
* Impliment `get_query` method

The method `get_query` should return select sql statement.  
You can write sql statement as raw sql or django model object.  

This is a simple example.  

```python
from django.db import models
from view_table.models import ViewTable


# Base table
class Book(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=100)


# View table
class Books(ViewTable):
    category = models.CharField(max_length=100)
    count = models.IntegerField()

    # You must implement get_query method.
    @classmethod
    def get_query(self):
        return Book.objects.values('category').annotate(count=models.Count('category')).query
        # You can also write:
        # return 'SELECT "polls_book"."category", COUNT("polls_book"."category") AS "count" FROM "polls_book" GROUP BY "polls_book"."category"' 
``` 


### Run command

After Django migration, you can create view tables the below command.  

```bash
python manage.py createviewtable
```

## License

MIT
