from django.shortcuts import render , redirect
from accounts.models import Day , Book
from django.views.generic import  DetailView 
from accounts.forms import Bookking
from django.views.generic.edit import FormMixin
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect


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
            existing_book = Book.objects.filter(day= myform.day,is_booked = False, date=myform.date).exists()
            existing = Book.objects.filter(user=request.user).exists()
            if existing:
                    messages.error(request, "you already booked.")
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
            if not existing_book:
                # Date hasn't been booked for the selected day, save the instance
                myform.is_booked = True
                myform.save()
                messages.success(request, "Booked Successfully .")
                return redirect('/')
            else:
                messages.error(request, "This date is already booked for that day .")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
                
        else:
            form=self.get_form()
    
def edit_book(request):
    book = Book.objects.filter(user=request.user).first()
    if request.method == "POST":
        form = Bookking(request.POST , instance=book)
        if form.is_valid():
            myform = form.save(commit=False)
            myform.user = request.user
            myform.save()
            messages.success(request, 'book updated successfully')
            return redirect(reverse('my_booking'))
    else:
        form = Bookking(instance=book)

    return render(request,'accounts/book_edit.html',{
        'form':form,
    })
