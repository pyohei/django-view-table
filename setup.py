from setuptools import setup

setup(
    name="django-view-table",
    version="1.0.1",
    packages=["view_table", "view_table.management.commands"],
    url="https://github.com/pyohei/django-view-table",
    license="MIT",
    author="Shohei Mukai",
    author_email="mukaishohei76@gmail.com",
    description="Django view table plugin",
    long_description=open("README.md", "r").read(),
    long_description_content_type="text/markdown",
)
