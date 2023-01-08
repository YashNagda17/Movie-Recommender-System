from django.urls import path
from forming import views

urlpatterns = [
    path('not/',views.default_page),
    path('form/',views.default_page),
    
    path('',views.default_page),

]
