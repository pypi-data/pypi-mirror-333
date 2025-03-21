# Algeria cities django package
Django package provides a complete list of all administrative provinces and cities in Algeria.

## Quick start
### Installation
Install the package using pip:
```shell
    pip install django-algeria-cities
```
### Configuration

1. Add "algeria_cities" to your INSTALLED_APPS in settings.py:
```py
    INSTALLED_APPS = [
        ...,
        "algeria_cities",
    ]
```

2. Run migrations to create the necessary database tables:
```shell
python manage.py migrate algeria_cities
```

## Credit
The data used in this package was sourced from [algeria-cities](https://github.com/othmanus/algeria-cities). Special thanks to the contributors of that project for their efforts in compiling and maintaining the dataset.