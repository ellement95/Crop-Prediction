import csv
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import *
from .forms import *
from django.core.paginator import Paginator , EmptyPage, PageNotAnInteger
import pandas as pd

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
            df = pd.DataFrame.from_records(CropData.objects.all().values())
            X_train, X_test, X_unseen, y_min_train, y_min_test, y_max_train, y_max_test, y_unseen = CropPricePrediction.preprocess_data(df)
            
            # Train and predict using the model's method
            mse_min, mse_max = CropPricePrediction.train_and_predict(X_train, X_test, X_unseen, y_min_train, y_max_train, y_min_test)
            
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