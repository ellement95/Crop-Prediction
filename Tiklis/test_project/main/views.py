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
                    year = int(date_string[0])
                    month = int(date_string[1])
                    day = int(date_string[2])
                    
                    try: 
                    # Check if the month is within the valid range
                        if month >= 1 or month <= 12:
                            # Create a datetime.date object
                            date_string = datetime(year, month, day).date()
                    except ValueError:
                        print(f"Invalid month value on: {date_string}")
                except ValueError:
                    print(f"Invalid date format on: {date_string}")
                    continue
                
                commodity = row[3]
                variety = row[4]
                classification = row[5]
                category = row[6]
                low_price = float(row[7])
                high_price = float(row[8])
                time_variable = row[9]
                try: 
                    time = datetime.strptime(time_variable, '%H:%M:%S').time()
                    
                    # Extract hour, minute, and second from the time_variable string
                    hour = int(time_variable.split(':')[0])
                    minute = int(time_variable.split(':')[1])
                    second = int(time_variable.split(':')[2])

                    # Create a datetime.time object
                    time_obj = datetime.time(hour, minute, second)
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