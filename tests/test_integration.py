from django.core.management import call_command
from django.db import connection, models
from django.test import TransactionTestCase

from view_table.models import ViewTable


class SourceBook(models.Model):
    category = models.CharField(max_length=100)

    class Meta:
        app_label = "tests"
        db_table = "tests_source_book"


class CategorySummary(ViewTable):
    category = models.CharField(max_length=100)
    count = models.IntegerField()

    class Meta:
        app_label = "tests"
        db_table = "tests_category_summary"
        managed = False

    @classmethod
    def get_query(cls):
        return str(
            SourceBook.objects.values("category")
            .annotate(count=models.Count("id"))
            .order_by("category")
            .query
        )


class CreateViewTableCommandTests(TransactionTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        with connection.schema_editor() as schema_editor:
            schema_editor.create_model(SourceBook)

    @classmethod
    def tearDownClass(cls):
        cls._drop_summary_view()
        with connection.schema_editor() as schema_editor:
            schema_editor.delete_model(SourceBook)
        super().tearDownClass()

    def setUp(self):
        super().setUp()
        self._drop_summary_view()
        SourceBook.objects.all().delete()

    @staticmethod
    def _drop_summary_view():
        with connection.cursor() as cursor:
            cursor.execute("DROP VIEW IF EXISTS tests_category_summary;")

    def test_createviewtable_creates_a_queryable_view(self):
        SourceBook.objects.bulk_create(
            [
                SourceBook(category="fiction"),
                SourceBook(category="fiction"),
                SourceBook(category="history"),
            ]
        )

        call_command("createviewtable", verbosity=0)

        rows = list(
            CategorySummary.objects.order_by("category").values_list(
                "category",
                "count",
            )
        )

        self.assertEqual(rows, [("fiction", 2), ("history", 1)])

    def test_createviewtable_registers_the_view_in_database(self):
        call_command("createviewtable", verbosity=0)

        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT name
                FROM sqlite_master
                WHERE type = 'view' AND name = 'tests_category_summary'
                """
            )
            row = cursor.fetchone()

        self.assertEqual(row, ("tests_category_summary",))
