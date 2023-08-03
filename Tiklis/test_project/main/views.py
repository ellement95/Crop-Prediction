from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import *
from .forms import *

# Create your views here.

def home(response):
	return render(response, "main/home.html", {})

def predict(request):
    if request.method == "POST":
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the uploaded file to the database using the File model
            file = form.cleaned_data['file']
            obj = File.objects.create(file=file)
            # Additional processing or computations can be performed here
            # For example, you can pass the 'obj' or its ID to the template
            # to display or manipulate it as needed
            return render(request, "main/prediction_result.html", {'file_obj': obj})
    else:
        form = FileUploadForm()

    return render(request, "main/predict.html", {'form': form})

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