from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import *
from .models import User
from django.shortcuts import render,redirect

def index(request):
    user = request.user
    bid_values = []
    if request.method == "POST":
        name = request.POST["entry_title"]
        desc = request.POST["description"]
        bid = request.POST["starting_bid"]
        url = request.POST["url"]
        category = request.POST["category"]
        l = Listing(user = user,title = name,description = desc, url = url,category=category)                        #Creating a listing
        l.save()
        b = Bid(listing = l, bid = bid,current_bidder = user )
        b.save()
    listings = Listing.objects.all()
    bid_objects = Bid.objects.all()
    for listing in listings:
        bid_object = bid_objects.get(listing = listing)
        bid_value = bid_object.bid
        bid_values.append(bid_value)
    print(bid_values)
    combined_list = zip(listings,bid_values)
    return render(request, "auctions/index.html",{
        "combined_list":combined_list
    }
    )


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
            user.watchlist.clear()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def create_listing(request):
    
    return render(request,"auctions/index.html",{
        "create":1
    })

def display_listing(request,listing_id):
    count,appear,closed,winner = 0,0,0,0
    listing = Listing.objects.get(id = listing_id)
    bid_object = Bid.objects.get(listing = listing)
    comments = Comments.objects.filter(listing = listing)
    user = request.user
    if user == listing.user:                            #To check whether the user requesting for the listing is the owner of the listing.
        closed = 1
    if listing.closed == 1:                             #To check if the auction has already been closed
        winner = 1
    if request.user.is_authenticated:                   #To check if item is in users watchlist
        for item in user.watchlist.all():
            if item != listing:
                count = count + 1
        if count ==  user.watchlist.count():
            appear = 1

    return render(request,"auctions/listing.html",{
        "listing":listing,
        "bid_object":bid_object,
        "appear": appear,
        "closed": closed,
        "winner": winner,
        "comments":comments
    })

def watchlist(request,listing_id):
    listing = Listing.objects.get(id = listing_id)
    print(listing_id)
    user = request.user
    print(user)
    print(user.watchlist.values())
    user.watchlist.add(listing)
    return redirect('listing', listing_id)

def remove_watchlist(request,listing_id):
    listing = Listing.objects.get(id = listing_id)
    print(listing_id)
    user = request.user
    print(user)
    print(user.watchlist.values())
    user.watchlist.remove(listing)
    return redirect('listing', listing_id)   

def bidding(request,listing_id):
    listing_obj = Listing.objects.get(id = listing_id)
    bid_object = Bid.objects.get(listing = listing_obj)
    user = request.user
    bid_value = request.POST["bid_value"]
    bid_value_con = int(bid_value)
    if bid_value_con > bid_object.bid:
        bid_object.bid = bid_value
        bid_object.current_bidder = user
        bid_object.save()
        return redirect('listing', listing_id)
    else:
        return render(request,"auctions/error.html",{
            "listing":listing_obj
        })

def close(request,listing_id):
    listing_obj = Listing.objects.get(id = listing_id)
    bid_object = Bid.objects.get(listing = listing_obj)
    listing_obj.closed = 1
    listing_obj.save()
    return redirect('listing', listing_id)

def comment(request,listing_id):
    listing_obj = Listing.objects.get(id = listing_id)
    user = request.user
    contents = request.POST["content"]
    new_comment = Comments(user=user,listing=listing_obj,content=contents)
    new_comment.save()
    return redirect('listing', listing_id)

def open_watchlist(request):
    user = request.user
    listings = user.watchlist.all()
    return render(request,"auctions/watchlist.html",{
        "listings":listings
    })

def categories(request):
    values_list = Listing.objects.values_list('category', flat=True)
    field_values = list(values_list)
    unique_list = list(set(field_values))
    print(unique_list)
    return render(request,"auctions/categories.html",{
        "category_list":unique_list
    })

def category_products(request,category):
    listings = Listing.objects.filter(category=category)
    return render(request,"auctions/categories.html",{
        "listings":listings,
        "category":category
    })
