from django.db import connection, models
from django.test import TransactionTestCase

from view_table.models import ViewTable


class Author(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        app_label = "tests"
        db_table = "tests_join_author"


class Publisher(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        app_label = "tests"
        db_table = "tests_join_publisher"


class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    # Not every book has a publisher on record -- exercises the LEFT JOIN.
    publisher = models.ForeignKey(Publisher, null=True, on_delete=models.SET_NULL)

    class Meta:
        app_label = "tests"
        db_table = "tests_join_book"


class AuthorPublisherSummary(ViewTable):
    """Mirrors real-world usage: a hand-written SQL string with several
    joins, rather than something built through the Django ORM."""

    # get_query() below synthesizes an id via ROW_NUMBER() -- without it,
    # Django's implicit "id" field would not match any column in the view.
    id = models.IntegerField(primary_key=True)
    author_name = models.CharField(max_length=100)
    publisher_name = models.CharField(max_length=100, null=True)
    book_count = models.IntegerField()

    class Meta:
        app_label = "tests"
        db_table = "tests_author_publisher_summary"
        managed = False

    @classmethod
    def get_query(cls):
        return """
            SELECT
                ROW_NUMBER() OVER (ORDER BY a.name, COALESCE(p.name, '')) AS id,
                a.name AS author_name,
                p.name AS publisher_name,
                COUNT(b.id) AS book_count
            FROM tests_join_book b
            INNER JOIN tests_join_author a ON a.id = b.author_id
            LEFT JOIN tests_join_publisher p ON p.id = b.publisher_id
            GROUP BY a.name, p.name
            ORDER BY a.name, COALESCE(p.name, '')
        """


class RawSqlJoinViewTableTests(TransactionTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        with connection.schema_editor() as schema_editor:
            schema_editor.create_model(Author)
            schema_editor.create_model(Publisher)
            schema_editor.create_model(Book)

    @classmethod
    def tearDownClass(cls):
        cls._drop_summary_view()
        with connection.schema_editor() as schema_editor:
            schema_editor.delete_model(Book)
            schema_editor.delete_model(Publisher)
            schema_editor.delete_model(Author)
        super().tearDownClass()

    def setUp(self):
        super().setUp()
        self._drop_summary_view()
        Book.objects.all().delete()
        Author.objects.all().delete()
        Publisher.objects.all().delete()

    @staticmethod
    def _drop_summary_view():
        with connection.cursor() as cursor:
            cursor.execute("DROP VIEW IF EXISTS tests_author_publisher_summary;")

    def test_createviewtable_resolves_joins_and_aggregates_correctly(self):
        herbert = Author.objects.create(name="Frank Herbert")
        orwell = Author.objects.create(name="George Orwell")
        independent = Author.objects.create(name="Independent Author")
        ace_books = Publisher.objects.create(name="Ace Books")
        secker = Publisher.objects.create(name="Secker & Warburg")

        Book.objects.bulk_create(
            [
                Book(title="Dune", author=herbert, publisher=ace_books),
                Book(title="Dune Messiah", author=herbert, publisher=ace_books),
                Book(title="1984", author=orwell, publisher=secker),
                # No publisher on record for this one -- must survive the
                # LEFT JOIN instead of disappearing from the results.
                Book(title="Self-Published Novel", author=independent, publisher=None),
            ]
        )

        from django.core.management import call_command

        call_command("createviewtable", verbosity=0)

        rows = list(
            AuthorPublisherSummary.objects.order_by("author_name").values_list(
                "author_name", "publisher_name", "book_count"
            )
        )

        self.assertEqual(
            rows,
            [
                ("Frank Herbert", "Ace Books", 2),
                ("George Orwell", "Secker & Warburg", 1),
                ("Independent Author", None, 1),
            ],
        )

    def test_summary_rows_have_a_working_synthetic_primary_key(self):
        herbert = Author.objects.create(name="Frank Herbert")
        ace_books = Publisher.objects.create(name="Ace Books")
        Book.objects.create(title="Dune", author=herbert, publisher=ace_books)

        from django.core.management import call_command

        call_command("createviewtable", verbosity=0)

        # A plain .all() (not .values_list()) must also work -- this is
        # only true because get_query() provides a real "id" column.
        summary = AuthorPublisherSummary.objects.get()
        self.assertEqual(summary.pk, 1)
        self.assertEqual(summary.author_name, "Frank Herbert")
