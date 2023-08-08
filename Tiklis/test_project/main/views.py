import csv
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import *
from .forms import *
from django.core.paginator import Paginator , EmptyPage, PageNotAnInteger
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# Create your views here.

def home(response):
	return render(response, "main/home.html", {})

def preprocess_data(df):
    # 1. Data Cleaning
    # Handle missing data (you can choose an appropriate imputation method):
    #df.fillna(df.mean(), inplace=True)

    # 2. Feature Selection/Extraction
    selected_features = df[["DATE", "PRICE (LOW)", "PRICE (HIGH)"]]

    # 3. Feature Scaling/Normalization
    # Scale the numerical features using StandardScaler:
    scaler = StandardScaler()
    selected_features = scaler.fit_transform(selected_features)

    # 4. Splitting the Data
    # Assuming you have a target variable 'target_column' in your DataFrame:
    target = df['target_column']
    X_train, X_test, y_train, y_test = train_test_split(selected_features, target, test_size=0.2, random_state=42)

    return X_train, X_test, y_train, y_test

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
            return render(request, 'main/upload_success.html')
    else:
        form = UploadFileForm()
    return render(request, "main/predict.html", {'form': form})

def weather(response):
    return render(response,"main/weather.html",{})

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