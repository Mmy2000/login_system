from django.shortcuts import render
from accounts.models import Day
from django.views.generic import  DetailView 

def home(request):
    days = Day.objects.all()
    context = {
        'days':days
    }
    return render(request, 'home.html' , context)

class DayDetail(DetailView):
    model = Day