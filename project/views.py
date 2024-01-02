from django.shortcuts import render , redirect
from accounts.models import Day , Book
from django.views.generic import  DetailView 
from accounts.forms import Bookking
from django.views.generic.edit import FormMixin
from django.urls import reverse
from django.contrib import messages


def home(request):
    days = Day.objects.all()
    context = {
        'days':days
    }
    return render(request, 'home.html' , context)

class DayDetail(FormMixin ,DetailView):
    model = Day
    form_class = Bookking

    def post(self , request , *args , **kwargs):
        form = self.get_form()
        if form.is_valid():
            myform = form.save(commit=False)
            myform.day= self.get_object()
            myform.user = request.user
            existing_book = Book.objects.filter(day= myform.day, date=myform.date).exists()
            if not existing_book:
                # Date hasn't been booked for the selected day, save the instance
                myform.save()
                messages.success(request, "Booked Successfully .")
                return redirect('/')
            else:
                messages.error(request, "This date is already booked for that day .")
                return redirect('/')
        else:
            form=self.get_form()

