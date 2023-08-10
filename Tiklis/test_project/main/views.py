import csv
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import *
from .forms import *
from django.core.paginator import Paginator , EmptyPage, PageNotAnInteger
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.linear_model import LinearRegression
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error, mean_absolute_error

# Create your views here.

def home(response):
	return render(response, "main/home.html", {})

def preprocess_data(df):
    # Extract relevant features from the timestamp columns
    df['YEAR'] = df['DATE'].dt.year
    df['MONTH'] = df['DATE'].dt.month
    df['DAY'] = df['DATE'].dt.day

    # Extract relevant features from the parsed time components
    df['HOUR'] = df['TIME'].apply(lambda x: x.hour)
    df['MINUTE'] = df['TIME'].apply(lambda x: x.minute)
    df['SECOND'] = df['TIME'].apply(lambda x: x.second)
        
    # Select categorical columns for one-hot encoding
    categorical_columns = ['COMMODITY', 'CLASSIFICATION', 'CATEGORY']

    # Apply one-hot encoding to categorical columns
    encoder = OneHotEncoder(drop='first', sparse=False)
    encoded_categorical = encoder.fit_transform(df[categorical_columns])

    # Create a DataFrame for encoded categorical features
    encoded_df = pd.DataFrame(encoded_categorical, columns=encoder.get_feature_names_out(input_features=categorical_columns))
    
    # Split the data into features and targets

    # Combine encoded categorical features with numerical features
    X = pd.concat([df[['YEAR', 'MONTH', 'DAY', 'HOUR', 'MINUTE', 'SECOND']], encoded_df], axis=1)

    y_min = df['MIN PRICE']  # Target: Minimum Price
    y_max = df['MAX PRICE']  # Target: Maximum Price

    # Split the data into training and testing sets
    X_train, X_test, y_min_train, y_min_test, y_max_train, y_max_test = train_test_split(X, y_min, y_max, test_size=0.2, random_state=42)

    # Split the data into training and testing sets
    X_train, X_test, y_min_train, y_min_test, y_max_train, y_max_test = train_test_split(X, y_min, y_max, test_size=0.2, random_state=42)

    # Split the testing data into validation and unseen test sets
    X_test, X_unseen, y_test, y_unseen = train_test_split(X_test, y_min_test, test_size=0.33, random_state=42)

    return X_train, X_test, X_unseen, y_min_train, y_min_test, y_max_train, y_max_test, y_unseen

def predict(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = form.cleaned_data['upload']
            
            file = uploaded_file.read().decode('utf-8')
            csv_reader = csv.reader(file.splitlines(), delimiter=',')
            next(csv_reader)

            for row in csv_reader:
                date = row[0]
                commodity = row[1]
                variety = row[2]
                classification = row[3]
                category = row[4]
                low_price = float(row[5])
                high_price = float(row[6])
                time_variable = row[7].strip()
                if len(row) >= 8:
                    CropData.objects.create(
                        date=date,
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
            
            # Preprocess the DataFrame
            X_train, X_test, X_unseen, y_min_train, y_min_test, y_max_train, y_max_test, y_unseen = preprocess_data(df)
            
            # Initialize StandardScaler
            scaler = StandardScaler()

            # Fit scaler on training data and transform all the splits
            X_train_scaled = scaler.fit_transform(X_train)
            X_test_scaled = scaler.transform(X_test)
            X_unseen_scaled = scaler.transform(X_unseen)
            
            # Linear Regression
    
            return render(request, 'main/upload_success.html')
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