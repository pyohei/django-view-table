# Example app

A small, runnable Django project that exercises `view_table` the way a
real consumer would -- as opposed to `tests/`, which only runs it through
Django's test runner. It implements the `Book`/`Books` example from the
top-level [README](../README.md).

## Run it

From the repository root:

```bash
pip install -r requirements.txt
pip install -e .
python example/manage.py migrate
python example/manage.py createviewtable
python example/manage.py runserver
```

Then open http://127.0.0.1:8000/. You should see the `Book` rows seeded by
a data migration, and a `Books` view aggregating them by category via
`view_table`.

If you change `Books.get_query()`, rerun `python example/manage.py
createviewtable` and reload the page -- the command drops and recreates the
view every time.
