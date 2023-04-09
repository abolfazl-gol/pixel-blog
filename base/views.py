from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from base.models import *
from account.models import *
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from base.forms import *
from .serializers import *
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class HomePage(APIView):
    def get(self, request):
        homepage = HomeSetting.objects.all()
        homepage = HomeSerializer(homepage).data
        return Response(homepage, status=status.HTTP_200_OK)

    def post(self):
        pass


def aboutusViwe(request):
    aboutus = Aboutus.objects.all()
    contex = {
        "aboutuslist": aboutus,
        "count": aboutus.count()
    }
    # text= """
    # <!DOCTYPE html>
    # <html>
    #     <head></head>
    #     <body>
    #         <h1> درباره ما <h1>
    #         <ul>
    #             {}
    #         <ul>
    #     </body>
    # </html>
    #
    # """ .format('\n'.join('<li>{}<li>'.format(about) for about in aboutus))
    return render(request, "base/aboutus.html", contex)


def homepageViwe(request):
    searchform = Search(request.GET)
    if searchform.is_valid():
        searchtext = searchform.cleaned_data["searchtext"]
        home = HomeSetting.objects.filter(superiority__contains=searchtext)

    else:
        home = HomeSetting.objects.all()

    contex = {
        "homelist": home,
        "searchform": searchform
    }

    return render(request, "base/homepage.html", contex)


@login_required()
def ticketViwe(request):
    # if request.user.is_staff and request.user.is_active:
    ticket = Ticket.objects.all()
    contex = {
        "ticketlist": ticket,
    }

    return render(request, "base/ticket.html", contex)


# else:
#     return HttpResponseRedirect(reverse(account.views.loginView))

def profileViwe(request, user_id):
    user = Profile.objects.get(pk=user_id)
    contex = {
        "userlist": user
    }
    return render(request, "base/user.html", contex)


def contactusViwe(request):
    contactus = Contactus.objects.all()
    contex = {
        "contactuslist": contactus,
    }

    return render(request, "base/contactus.html", contex)


def ticketeditViwe(request):
    # ticketform = TicketEd(request.GET)
    # sendticket = ticketform(request.POST, instance=ticketform)
    if request.method == "POST":
        sendticket = TicketEd(request.POST)
        if sendticket.is_valid():
            sendticket.save()
            return HttpResponseRedirect(reverse(ticketViwe))

    contex = {
        "sendticket": sendticket,
    }

    return render(request, "base/ticketedit.html", contex)
