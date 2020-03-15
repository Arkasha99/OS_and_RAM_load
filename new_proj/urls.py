from django.urls import path

from new_proj.views import *

urlpatterns=[
    path('load-average/',load_average, name='load-average'),
    path('ram/', ram, name='ram'),
    path('login/',user_login, name='login'),
    path('logout/',logout, name='logout'),
]