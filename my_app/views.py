from django.shortcuts import render
from .forms import MLfileForm,DataForm
from .models import MLmodel
import pandas as pd
import pickle
from statsmodels.tsa.arima.model import ARIMA
import statsmodels.api as sm
import pyrebase
import os
from django.core.files.storage import default_storage
from django.contrib import messages

config = {
     "apiKey": "AIzaSyALrKiQ_ZPzJcv_hSfCOU1Wno7eV6JduSU",
  "authDomain": "mtp1-e4aba.firebaseapp.com",
  "projectId": "mtp1-e4aba",
  "storageBucket": "mtp1-e4aba.appspot.com",
  "messagingSenderId": "244120426233",
  "appId": "1:244120426233:web:eb46e01327cdcb1cd03428",
  "measurementId": "G-8FHX55N98B",
      "databaseURL": "",
}

firebase = pyrebase.initialize_app(config)
storage = firebase.storage()

def preprocess(dataset_path,classifier_path):
    df = pd.read_csv('media\data_file'+'\\'+str(dataset_path),index_col='date',parse_dates=True)
    # media\seq\2-8-pro-nested_Probio651.csv
    classifier = pickle.load(open('media\ml_model'+'\\'+str(classifier_path), 'rb'))
    # df = pd.read_csv('/content/DATASET.csv', index_col='date',parse_dates=True)
    df = df.dropna()
    columns_to_drop = [ "ID","Longitude", "Latitude"]
    df = df['Tem_IN (C)']
    print(df)
    start_time = '2023-04-26 16:25:00'
    end_time = '2023-04-26 17:15:00'
    timestamps = pd.date_range(start=start_time, end=end_time,freq='10T')
    # classifier = pickle.load(open('/content/model.pkl', 'rb'))
    pred=classifier.predict(start=len(df),end=len(df)+len(timestamps)-1,typ='levels').rename('ARIMA Predictions')
    pred.index = timestamps
    # temp_in = classifier.predict(df)
    return pred.index,pred.values

# Create your views here.
def home(request):
    return render(request,'my_app/home.html')

def classify(request):
    model_call = MLfileForm()
    seq_call = DataForm()
    param = {"sequence_file_input":seq_call,'model_file_input':model_call}
    return render(request,'my_app/classify.html',param)

def predict(request):
    if request.method == "POST":
        print(1)
        model_call = MLfileForm(request.POST,request.FILES)
        seq_call = DataForm(request.POST,request.FILES)
        print(request.FILES)
        seq_path = request.FILES['data']
        model_path = request.FILES['ml_file']
        ml_file = request.FILES['ml_file']
        file_save = default_storage.save(ml_file.name, ml_file)
        storage.child("files/" + ml_file.name).put("media/" + ml_file.name)
        delete = default_storage.delete(ml_file.name)
        messages.success(request, "File upload in Firebase Storage successful")
        if model_call.is_valid():
            model_call.save()
        if seq_call.is_valid():
            seq_call.save()
            
    print(model_path)
    print(seq_path)

    index,temp_in= preprocess(seq_path,model_path)
    # pred = output(y_pred)
    # print(assembly_accession)
    elements = list(zip(index,temp_in))
    param = {"sequence_file_input":seq_call,'model_file_input':model_call,'elements':elements}
    return render(request,'my_app/predict.html',param)