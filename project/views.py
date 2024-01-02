from django.shortcuts import render , redirect
from accounts.models import Day
from django.views.generic import  DetailView 
from accounts.forms import Book
from django.views.generic.edit import FormMixin
from django.urls import reverse

def home(request):
    days = Day.objects.all()
    context = {
        'days':days
    }
    return render(request, 'home.html' , context)

class DayDetail(FormMixin ,DetailView):
    model = Day
    form_class = Book

    def post(self , request , *args , **kwargs):
        form = self.get_form()
        if form.is_valid():
            myform = form.save(commit=False)
            myform.day= self.get_object()
            myform.user = request.user
            myform.save()

            return redirect('/')