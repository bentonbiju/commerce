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
    path("open_watchlist",views.open_watchlist, name = "open_watchlist"),
    path("categories",views.categories, name = "categories"),
    path("categories/<str:category>",views.category_products, name = "cat_products"),
    path("listing/<str:listing_id>",views.display_listing, name = "listing"),
    path("listing/<str:listing_id>/bid",views.bidding, name = "bidding"),
    path("listing/<str:listing_id>/close",views.close, name = "close"),
    path("listing/<str:listing_id>/comment",views.comment, name = "comment"),
    path("watchlist/<str:listing_id>",views.watchlist,name = "watchlist"),
    path("remove_watchlist/<str:listing_id>",views.remove_watchlist,name = "remove_watchlist"),
]
