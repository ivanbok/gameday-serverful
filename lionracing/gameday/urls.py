from django.urls import path, include

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("index", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("viewrace", views.viewrace, name="viewrace"),
    path("viewbetslist", views.viewbetslist, name="viewbetslist"),
    path("viewbetresults", views.viewbetresults, name="viewbetresults"),
    path("calendar", views.calendar, name="calendar")
]
