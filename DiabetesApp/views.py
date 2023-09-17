from django.shortcuts import render
from DiabetesApp.models import users
# Create your views here.
import pandas as pd
import seaborn as sb
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import numpy as np
def loginview(request):
    return render(request,'login.html')

def registrationview(request):
    return  render(request,'registration.html')

def saveuserview(request):
    username=request.POST['username']
    password = request.POST['password']
    name = request.POST['name']
    email = request.POST['email']
    phone = request.POST['phone']
    address = request.POST['address']

    newusers=users(username=username,password=password,name=name,email=email,phone=phone,address=address)
    newusers.save()
    return render(request, 'login.html')

def verifyuserview(request):
    username=request.POST["username"]
    password=request.POST["password"]

    user= users.objects.filter(username=username)

    for u in user:
        if u.password==password:
            return render(request,'home.html')
        else:
            return render(request, 'login.html')

def homeview(request):
    return render(request,'home.html')
def resultview(request):
    pregnancies=request.POST['prgnancies']
    glucose=request.POST['glucose']
    bp = request.POST['bp']
    skin = request.POST['skin']
    insulin = request.POST['insulin']
    dpd = request.POST['dpd']
    bmi = request.POST['bmi']
    age = request.POST['age']



    dataset = pd.read_csv("diabetes.csv")  # read csv file
    q1 = 62
    q3 = 80
    IQR = q3 - q1
    lowerlimit = q1 - 1.5 * IQR
    upperlimit = q3 + 1.5 * IQR
    new_iqr = dataset[(dataset['BloodPressure'] > lowerlimit) & (dataset['BloodPressure'] < upperlimit)]
    x = new_iqr.iloc[:, :-1]  # split data
    y = new_iqr.iloc[:, -1]

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.10)  # split train and test
    model = RandomForestClassifier(random_state=48)  # create model
    # values=[6,137,90,45,0,33.6,0.627,50]
    values = [pregnancies, glucose, bp, skin, insulin, dpd, bmi, age]
    values = np.reshape(values, (1, -1))
    model.fit(x_train.values, y_train.values)  # fit into model
    predicted_result = model.predict(values)  # predict outcome

    if predicted_result[0] == 0:
        result="You are normal"

    else:
        result='You have diabetes'

    return render(request, 'result.html',{'result':result})


