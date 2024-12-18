
from django.db import models
from django.contrib.auth.models import User
import pyotp

class Book(models.Model):
    title=models.TextField("Наименование")
    year_of_publication=models.IntegerField("Год публикации")
    
    author_FK=models.ForeignKey("Author",on_delete=models.CASCADE,null=True,verbose_name="Автор")
    matter_FK=models.ForeignKey("Matter",on_delete=models.CASCADE,null=True,verbose_name="Жанр")
    form_FK=models.ForeignKey("Form",on_delete=models.CASCADE,null=True,verbose_name="Форма")
    kind_FK=models.ForeignKey("Kind",on_delete=models.CASCADE,null=True,verbose_name="Род")
    publishingHouse_FK=models.ForeignKey("PublishingHouse",on_delete=models.CASCADE,null=True,verbose_name="Издательство")

    user = models.ForeignKey("auth.User", verbose_name="Пользователь", on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name="Книга"
        verbose_name_plural="Книги"

    def __str__(self) -> str:
        return self.title

class Author(models.Model):
    name=models.TextField("Имя")
    surname=models.TextField("Фамилия")
    patronymic=models.TextField("Отчество")
    years_of_life=models.TextField("Годы жизни")

    # добавим ImageField, в upload_to указываем папку куда загружать файл
    picture = models.ImageField("Изображение", null=True, upload_to="authors")

    user = models.ForeignKey("auth.User", verbose_name="Пользователь", on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name="Автор"
        verbose_name_plural="Авторы"
    
    def __str__(self) -> str:
        return self.name+" "+self.surname+" "+self.patronymic
    


class Matter(models.Model):
    title=models.TextField("Название жанра")

    user = models.ForeignKey("auth.User", verbose_name="Пользователь", on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name="Вид содержания"
        verbose_name_plural="Виды содержания"

    def __str__(self) -> str:
        return self.title

class  PublishingHouse(models.Model):
    name=models.TextField("Название издательства")
    year_of_foundation=models.IntegerField("Год основания")

    # добавим ImageField, в upload_to указываем папку куда загружать файл
    picture = models.ImageField("Изображение", null=True, upload_to="publishingHouses")

    user = models.ForeignKey("auth.User", verbose_name="Пользователь", on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name="Издательство"
        verbose_name_plural="Издательства"

    def __str__(self) -> str:
        return self.name

class Form(models.Model):
    name=models.TextField("Форма написания")

    user = models.ForeignKey("auth.User", verbose_name="Пользователь", on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name="Форма написания"
        verbose_name_plural="Формы написания"

    def __str__(self) -> str:
        return self.name

class Kind(models.Model):
    name=models.TextField("Форма написания")

    user = models.ForeignKey("auth.User", verbose_name="Пользователь", on_delete=models.CASCADE, null=True)

    
    class Meta:
        verbose_name="Род литературы"
        verbose_name_plural="Роды литературы"

    def __str__(self) -> str:
        return self.name
    

class UserProfile(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    opt_key=models.CharField(max_length=32, default=pyotp.random_base32)
    def __str__(self):
        return self.user.username
    
    