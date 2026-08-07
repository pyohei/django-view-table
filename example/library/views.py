from django.db.utils import OperationalError
from django.shortcuts import render

from library.models import AuthorPublisherSummary, Book, Books


def index(request):
    books = Book.objects.order_by("category", "name")

    try:
        summaries = list(Books.objects.order_by("category"))
        view_missing = False
    except OperationalError:
        summaries = []
        view_missing = True

    try:
        author_publisher_summaries = list(
            AuthorPublisherSummary.objects.order_by("author_name")
        )
    except OperationalError:
        author_publisher_summaries = []
        view_missing = True

    return render(
        request,
        "library/index.html",
        {
            "books": books,
            "summaries": summaries,
            "author_publisher_summaries": author_publisher_summaries,
            "view_missing": view_missing,
        },
    )
