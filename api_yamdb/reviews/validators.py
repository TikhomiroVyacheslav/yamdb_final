import datetime as dt

from rest_framework import serializers


def validate_title_year(value):
    year = dt.date.today().year
    if value > year:
        raise serializers.ValidationError('Проверьте год произведения!')
    return value
