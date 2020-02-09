from django.core.management.base import BaseCommand
from django.db import connection

from view_table.models import ViewTable


class Command(BaseCommand):

    def handle(self, *args, **options):
        for target in ViewTable.__subclasses__():
            table = target._meta.db_table
            query = target.get_query()
            with connection.cursor() as cursor:
                self.drop(cursor, table)
                self.create(cursor, table, query)

    def drop(self, cursor, table):
        cursor.execute('DROP VIEW IF EXISTS {};'.format(table))

    def create(self, cursor, table, query):
        cursor.execute('CREATE VIEW {table} AS {query};'.format(
            table=table, query=query
        ))
