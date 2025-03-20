# Djaport (Reports for tests in Django)


A package that will allow you to generate test reports of the tests that you have added in Django project.


You can track test by simply adding the following annotation in your test file:
```python
    @tag('<tag-name>')
    @djaport_test(
        category='<test-category>',
        author='<author-name>',
        description='<description>'
    )
```

and run your test like:

```shell
python manage.py test --testrunner=djaport.runner.CustomTestRunner
```
