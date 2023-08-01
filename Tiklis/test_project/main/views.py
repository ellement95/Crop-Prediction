from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import *
from .forms import *

# Create your views here.

def home(response):
	return render(response, "main/home.html", {})

def predict(request):
    if request.method == "POST":
        file = request.FILES['file']
        obj = File.objects.create(file=file)
        
  
    return render(request,"main/predict.html",{})

def weather(response):
    return render(response,"main/weather.html",{})

def crops(response):
    return render(response,"main/crops.html",{})
            
def create(response):
	if response.method == "POST":
		form = CreateNewList(response.POST)

		if form.is_valid():
			n = form.cleaned_data["name"]
			t = ToDoList(name=n)
			t.save()

		return HttpResponseRedirect("/%i" %t.id)
	else:
		form = CreateNewList()
	return render(response, "main/create.html", {"form":form})

def test(request):
	return render(request,'main/test.html')