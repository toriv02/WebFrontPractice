from datetime import date, timedelta
import locale
from typing import Any
from django.core.management.base import BaseCommand

from faker import Faker
import random
from content.models import *

class Command(BaseCommand):
    def handle(self, *args, **options):
        fake=Faker(['ru_RU'])
        for _ in range(1):
            fio=fake.name().split()

            start_date = date(1700, 1, 1)
            end_date = date(1900, 1, 1)
            time_between_dates = end_date - start_date
            days_between_dates = time_between_dates.days
            random_number_of_days = random.randrange(days_between_dates)
            birthdate = start_date + timedelta(days=random_number_of_days)

            deathdate = birthdate + timedelta(days=random.randint(10000, 30000)) 
            locale.setlocale(locale.LC_TIME, 'ru_RU')


            years_of_life = f"{birthdate.strftime('%d %B %Y')} — {deathdate.strftime('%d %B %Y')}"


            Author.objects.create(
                name=fio[2],
                surname=fio[0],
                patronymic=fio[1],
                years_of_life=years_of_life
            )