from typing import Any
from django.shortcuts import render
from django.http import HttpResponse
from django.views import View

from content.models import Book
from django.views.generic import TemplateView


# Create your views here.
class ShowBooksView(View):

    def get(request, *args,**kwargs):
        books=Book.objects.all()

        result=""
        for b in books:
            result+=b.title+"<br>"
        return HttpResponse(result)

        
class ShowBooksView(TemplateView):        
    template_name="books/show_books.html"

    def get_context_data(self, **kwargs: Any) -> dict[str,Any]:
       context=super().get_context_data(**kwargs)
       context['books']=Book.objects.all()

       return context

