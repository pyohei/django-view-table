from django.db import models

from view_table.models import ViewTable


# Base table
class Book(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=100)

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
