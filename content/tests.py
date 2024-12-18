from django.test import TestCase
from rest_framework.test import APIClient
from model_bakery import baker

from content.models import Book,Matter,Form,Kind,PublishingHouse,Author
# Create your tests here.
class BooksViewsetTestaseCase(TestCase):
    def setUp(self):
        self.client=APIClient()
    
    def test_get_list(self):
        mt = Matter.objects.create(
            title= "комедия"
        )
        fr=Form.objects.create(
            name= "пьеса"
        )
        kd=Kind.objects.create(
            name= "драма"
        )
        au=Author.objects.create(
            name= "Александр",
            surname= "Сергеевич",
            patronymic= "Грибоедов",
            years_of_life= "5 января 1795 — 11 февраля 1829"
        )
        pb=PublishingHouse.objects.create(
            name= "типография Августа Семена",
            year_of_foundation= 1818
        )
        book=Book.objects.create(
            title= "Горе от ума",
            year_of_publication= 1833,
            author=au,
            matter=mt,
            form=fr,
            kind=kd,
            publishingHouse=pb,
        )
            
        r=self.client.get('/api/books/')
        data=r.json()
        print(data)
        assert book.id==data[0]['id']
        assert book.title==data[0]['title']

        #assert book.author.id==data[0]['author']
        #assert book.matter.id==data[0]['matter']
        #assert book.form.id==data[0]['form']
        #assert book.kind.id==data[0]['kind']
        #assert book.publishingHouse.id==data[0]['publishingHouse']

        assert len(data)==1

        

      
        
        
    


