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

Then open http://127.0.0.1:8000/. You should see:

* `Book` -- the regular table.
* `Books` -- a view aggregating `Book` by category, with `get_query()`
  built through the Django ORM query builder.
* `AuthorPublisherSummary` -- a view backed by a hand-written SQL string
  joining `Book`, `Author`, and `Publisher` (`INNER JOIN` + `LEFT JOIN` +
  `GROUP BY`), closer to how view_table tends to be used in practice.

If you change a model's `get_query()`, rerun `python example/manage.py
createviewtable` and reload the page -- the command drops and recreates
every view each time.
