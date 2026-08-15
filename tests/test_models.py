from django.test import SimpleTestCase

from view_table.models import ViewTable


class ViewTableModelTests(SimpleTestCase):
    def test_viewtable_is_abstract_and_unmanaged(self):
        self.assertTrue(ViewTable._meta.abstract)
        self.assertFalse(ViewTable._meta.managed)

    def test_get_query_must_be_implemented_by_subclasses(self):
        with self.assertRaises(NotImplementedError):
            ViewTable.get_query()
