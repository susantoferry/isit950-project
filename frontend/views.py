from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, "isit950/index.html")

def login_view(request):
    if request.method == "POST":
        # case insensitive username to login
        username = User.objects.values_list('username', flat=True).get(username__icontains=request.POST["username"].lower())
        # Attempt to sign user in
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            # request.session['fav_color'] = 'blue'
            # <li>{{ request.session.fav_color }}</li>
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "admin_piano/account/login.html", {
                "message": "Invalid username and/or password.",
                "status": "danger"
            })
    else:
        return render(request, "admin_piano/account/login.html")

def logoutV(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))