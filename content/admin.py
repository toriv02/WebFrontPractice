from django.contrib import admin

from content.models import Book
from content.models import Author
from content.models import Matter
from content.models import PublishingHouse
from content.models import Form
from content.models import Kind
# Register your models here.
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display=['id','title','year_of_publication','matter_FK','form_FK','kind_FK','author_FK','publishingHouse_FK']

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display=['id','name','surname','patronymic','years_of_life']

@admin.register(Matter)
class MatterAdmin(admin.ModelAdmin):
    list_display=['id','title']

@admin.register(PublishingHouse)
class HouseAdmin(admin.ModelAdmin):
    list_display=['id','name','year_of_foundation']

@admin.register(Form)
class FormAdmin(admin.ModelAdmin):
    list_display=['id','name']


@admin.register(Kind)
class KindAdmin(admin.ModelAdmin):
    list_display=['id','name']
