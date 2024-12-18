"""
URL configuration for app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static

from content import views
from rest_framework.routers import DefaultRouter

from content.api import BooksViewset,KindsViewset,AuthorsViewset,FormsViewset,PublishingHousesViewset,MattersViewset,UserViewSet

router=DefaultRouter()
router.register("books",BooksViewset, basename="books")
router.register("kinds",KindsViewset, basename="kinds")
router.register("authors",AuthorsViewset, basename="authors")
router.register("forms",FormsViewset,basename="forms")
router.register("publishinghouses",PublishingHousesViewset,basename="publishinghouses")
router.register("matters",MattersViewset,basename="matters")
router.register("user",UserViewSet,basename="user")

urlpatterns = [
    path('',views.ShowBooksView.as_view()),
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
