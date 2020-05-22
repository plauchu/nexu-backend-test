from django.urls import path
from nexu_api import views

urlpatterns =[
    path('brands/', views.ApiViewBrand.as_view()),
    path('models/', views.ApiViewModel.as_view()),
]
