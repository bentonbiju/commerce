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
    if request.method == "POST":
        name = request.POST["entry_title"]
        desc = request.POST["description"]
        bid = request.POST["starting_bid"]
        url = request.POST["url"]
        l = Listing(user = user,title = name,description = desc, url = url)                        #Creating a listing
        l.save()
        b = Bid(user = user, listing = l, bid = bid,current_bidder = user )
        b.save()
    listings = Listing.objects.all()
    return render(request, "auctions/index.html",{
        "listings": listings 
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
    listing = Listing.objects.get(id = listing_id)
    bid_object = Bid.objects.get(listing = listing)
    user = request.user
    count = 0
    appear = 0
    if request.user.is_authenticated:
        for item in user.watchlist.all():
            if item != listing:
                count = count + 1
        if count ==  user.watchlist.count():
            appear = 1
    return render(request,"auctions/listing.html",{
        "listing":listing,
        "bid_object":bid_object,
        "appear": appear
    })

def watchlist(request,listing_id):
    listing = Listing.objects.get(id = listing_id)
    print(listing_id)
    user = request.user
    print(user)
    print(user.watchlist.values())
    user.watchlist.add(listing)
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

    