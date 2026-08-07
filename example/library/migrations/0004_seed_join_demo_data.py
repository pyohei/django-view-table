from django.db import migrations


def seed_join_demo_data(apps, schema_editor):
    Author = apps.get_model("library", "Author")
    Publisher = apps.get_model("library", "Publisher")
    Book = apps.get_model("library", "Book")

    herbert = Author.objects.create(name="Frank Herbert")
    orwell = Author.objects.create(name="George Orwell")
    independent = Author.objects.create(name="Independent Author")
    ace_books = Publisher.objects.create(name="Ace Books")
    secker = Publisher.objects.create(name="Secker & Warburg")

    Book.objects.bulk_create(
        [
            Book(
                name="Dune",
                category="Sci-Fi",
                author=herbert,
                publisher=ace_books,
            ),
            Book(
                name="Dune Messiah",
                category="Sci-Fi",
                author=herbert,
                publisher=ace_books,
            ),
            Book(
                name="Nineteen Eighty-Four",
                category="Fiction",
                author=orwell,
                publisher=secker,
            ),
            # No publisher on record -- exercises the LEFT JOIN in
            # AuthorPublisherSummary.get_query().
            Book(
                name="Self-Published Novel",
                category="Fiction",
                author=independent,
                publisher=None,
            ),
        ]
    )


def unseed_join_demo_data(apps, schema_editor):
    Book = apps.get_model("library", "Book")
    Author = apps.get_model("library", "Author")
    Publisher = apps.get_model("library", "Publisher")

    Book.objects.filter(
        name__in=[
            "Dune",
            "Dune Messiah",
            "Nineteen Eighty-Four",
            "Self-Published Novel",
        ]
    ).delete()
    Author.objects.filter(
        name__in=["Frank Herbert", "George Orwell", "Independent Author"]
    ).delete()
    Publisher.objects.filter(name__in=["Ace Books", "Secker & Warburg"]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("library", "0003_add_author_publisher"),
    ]

    operations = [
        migrations.RunPython(seed_join_demo_data, unseed_join_demo_data),
    ]
