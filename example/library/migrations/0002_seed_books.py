from django.db import migrations

BOOKS = [
    ("Clean Code", "Engineering"),
    ("The Pragmatic Programmer", "Engineering"),
    ("Designing Data-Intensive Applications", "Engineering"),
    ("Dune", "Sci-Fi"),
    ("Foundation", "Sci-Fi"),
    ("1984", "Fiction"),
]


def seed_books(apps, schema_editor):
    Book = apps.get_model("library", "Book")
    Book.objects.bulk_create(
        [Book(name=name, category=category) for name, category in BOOKS]
    )


def unseed_books(apps, schema_editor):
    Book = apps.get_model("library", "Book")
    Book.objects.filter(name__in=[name for name, _ in BOOKS]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("library", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(seed_books, unseed_books),
    ]
