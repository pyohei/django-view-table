from django.db import models

from view_table.models import ViewTable


class Author(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Publisher(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# Base table
class Book(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    # Nullable: only books added for the AuthorPublisherSummary demo below
    # have these set, so the join view has a NULL publisher to resolve.
    author = models.ForeignKey(
        Author, null=True, blank=True, on_delete=models.SET_NULL, related_name="books"
    )
    publisher = models.ForeignKey(
        Publisher, null=True, blank=True, on_delete=models.SET_NULL, related_name="books"
    )

    def __str__(self):
        return self.name


# View table
#
# get_query() only selects category/count, so the model must not rely on
# Django's implicit auto "id" column -- the view has no such column.
# Marking category as the primary key avoids that mismatch.
class Books(ViewTable):
    category = models.CharField(max_length=100, primary_key=True)
    count = models.IntegerField()

    # You must implement get_query method.
    @classmethod
    def get_query(cls):
        return str(
            Book.objects.values("category")
            .annotate(count=models.Count("category"))
            .order_by("category")
            .query
        )

    def __str__(self):
        return "{} ({})".format(self.category, self.count)


# View table backed by hand-written SQL with several joins, rather than a
# query built through the Django ORM -- this is the shape most real-world
# view_table usage takes.
class AuthorPublisherSummary(ViewTable):
    # ROW_NUMBER() in get_query() synthesizes this id -- without it,
    # Django's implicit "id" field would not match any column in the view
    # (see Books above for the simpler version of this same problem).
    id = models.IntegerField(primary_key=True)
    author_name = models.CharField(max_length=100)
    publisher_name = models.CharField(max_length=100, null=True)
    book_count = models.IntegerField()

    class Meta:
        managed = False

    @classmethod
    def get_query(cls):
        return """
            SELECT
                ROW_NUMBER() OVER (ORDER BY a.name, COALESCE(p.name, '')) AS id,
                a.name AS author_name,
                p.name AS publisher_name,
                COUNT(b.id) AS book_count
            FROM library_book b
            INNER JOIN library_author a ON a.id = b.author_id
            LEFT JOIN library_publisher p ON p.id = b.publisher_id
            GROUP BY a.name, p.name
            ORDER BY a.name, COALESCE(p.name, '')
        """

    def __str__(self):
        return "{} / {} ({})".format(
            self.author_name, self.publisher_name, self.book_count
        )
