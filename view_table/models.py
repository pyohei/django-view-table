from abc import abstractmethod

from django.db import models


class ViewTable(models.Model):

    class Meta:
        managed = False
        abstract = True

    @classmethod
    @abstractmethod
    def get_query(self):
        raise NotImplementedError('Not exists select query.')