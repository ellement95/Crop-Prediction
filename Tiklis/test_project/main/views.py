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
                    date = datetime.strptime(date_string, '%Y-%m-%d').date()
                    
                    # Extract year, month, and day from the components
                    year = date.year
                    month = date.month
                    day = date.day
                    
                    try: 
                        # Check if the month is within the valid range
                        if month >= 1 and month <= 12:
                            # Create a datetime.date object
                            date_string = date
                    except ValueError:
                        print(f"Invalid month value on: {date_string}")
                except ValueError:
                    print(f"Invalid date format on: {date_string}")
                    continue
                
                commodity = row[1]
                variety = row[2]
                classification = row[3]
                category = row[4]
                low_price = float(row[5])
                high_price = float(row[6])
                time_variable = row[7]
                try: 
                    time = datetime.strptime(time_variable, '%H:%M:%S').time()
                    
                    hour = time.hour
                    minute = time.minute
                    second = time.second
                    
                    # Create a datetime.time object
                    time_variable = time
                except ValueError:
                    print(f"Invalid time format on: {time_variable}")
                    continue
                
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
                    
            else:  # User input form submission
                form = UserInputForm(request.POST)
                if form.is_valid():
                    # Collect user inputs from the form
                    user_input = form.cleaned_data

                    # Process the uploaded CSV file
                    if 'upload' in request.FILES:
                        uploaded_file = request.FILES['upload']
                        df = pd.read_csv(uploaded_file)
                        df = CropPricePrediction.convert_date_and_time(df)

                        # Make predictions based on user input
                        predicted_min_price, predicted_max_price = CropPricePrediction.predict_price(user_input, df)
                        
                        # Render the results
                        return render(request, 'main/prediction_results.html', {
                            'predicted_min_price': predicted_min_price,
                            'predicted_max_price': predicted_max_price,
                            'user_input': user_input,
                        })

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