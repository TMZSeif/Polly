from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('create/', views.create, name="create"),
    path('view/', views.view, name="view"),
    path("password_reset/", views.password_reset_request, name="password_reset"),
    path('view/<int:id>', views.view_poll, name="view_poll"),
    path("<int:id>/", views.poll, name="poll"),
    path("<int:id>/results", views.results, name="results"),
    path("create/<int:id>", views.url, name="url")
]