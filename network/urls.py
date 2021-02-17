from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),

    # API
    path("add_post", views.add_post, name="add_post"),
    path("post/<int:post_id>", views.post, name="post" ),
    path("<str:nav_bar>", views.nav_bar, name="links"),
    path("profile/<str:user_profile>", views.profile, name='profile')
]
