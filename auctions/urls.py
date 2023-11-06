from django.urls import path

from . import views
from django.contrib import admin
urlpatterns = [
    path("admin/",admin.site.urls),
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing",views.create_listing, name = "create"),
    path("listing/<str:listing_id>",views.display_listing, name = "listing"),
    path("listing/<str:listing_id>/bid",views.bidding, name = "bidding"),
    path("watchlist/<str:listing_id>",views.watchlist,name = "watchlist")
]
