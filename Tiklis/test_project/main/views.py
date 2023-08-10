import csv
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import *
from .forms import *
from django.core.paginator import Paginator , EmptyPage, PageNotAnInteger
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error, mean_absolute_error
from datetime import datetime 
# Create your views here.

def home(response):
	return render(response, "main/home.html", {})

def predict(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = form.cleaned_data['upload']
            
            file = uploaded_file.read().decode('utf-8')
            csv_reader = csv.reader(file.splitlines(), delimiter=',')
            next(csv_reader)

            for row in csv_reader:
                date_string = row[0]
                try: 
                    date = datetime.strptime(date_string, '%m/%d/%Y').date()
                except ValueError:
                    print(f"Invalid date format on: {date_string}")
                    continue
                
                commodity = row[1]
                variety = row[2]
                classification = row[3]
                category = row[4]
                low_price = float(row[5])
                high_price = float(row[6])
                time_variable = row[7].strip()
                if len(row) >= 8:
                    CropData.objects.create(
                        date=date_string,
                        commodity=commodity,
                        variety=variety,
                        classification=classification,
                        category=category,
                        low_price=low_price,
                        high_price=high_price,
                        time_variable=time_variable
                    )
                else:
                    print("something wrong", row)
                    
            # # Use the CropPricePrediction class to predict price categories
            # crop_price_predictor = CropPricePrediction()
            # X_train, X_test, y_train, y_test = crop_price_predictor.preprocess_data(CropData.objects.all())
            # model, accuracy = crop_price_predictor.train_and_predict(X_train, X_test, y_train)

            # # Process user inputs
            # user_input = {
            #     'date': request.POST['date'],  # Extract from your form fields
            #     'commodity': request.POST['commodity'],
            #     'classification': request.POST['classification'],
            #     'category': request.POST['category'],
            #     'time_variable': request.POST['time_variable']
            # }
            
            # # Get formatted user input data
            # input_data = crop_price_predictor.get_user_input_data(user_input)
            
            # predicted_category = crop_price_predictor.predict_price_category([input_data], model, accuracy)
            
            return render(request, 'main/upload_success.html', {})
    else:
        form = UploadFileForm()
    return render(request, "main/predict.html", {'form': form})

def weather(response):
    return render(response,"main/weather.html",{})

def graphs(response):
    return render(response,"main/graphs.html",{})

def crops(request):
    crop = CropData.objects.all().order_by('date')
    page = request.GET.get('page',1)

    paginator = Paginator(crop,10)
    try:
         crop = paginator.page(page)
    except PageNotAnInteger:
         crop = paginator.page(1)
    except EmptyPage:
         crop = paginator.page(paginator.num_pages)
    return render(request, "main/crops.html", {'crop': crop})
            

def test(request):
	return render(request,'main/test.html')