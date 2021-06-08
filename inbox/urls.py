
from django.urls import path , include

from . import views

urlpatterns = [
    path('' , views.index , name='Index_Page'),
    path('<str:room_name>/' , views.Inbox , name='Inbox_Page')
]
