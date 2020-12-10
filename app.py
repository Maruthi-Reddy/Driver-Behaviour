# -*- coding: utf-8 -*-
import pickle
import requests
import numpy as np
import pygal
import csv
import pandas as pd
from flask import Flask,jsonify ,render_template, request


app = Flask(__name__)
model = pickle.load(open('model.pickle', 'rb'))

@app.route('/',methods=['GET','POST'])
def home():
    return render_template('index.html')


@app.route('/data',methods=['GET','POST'])
def predict_file():
    if request.method=='POST':
        f=request.form['csvfile']
        data=[]
        with open(f) as file:
            csvfile=csv.reader(file)
            for row in csvfile:
                data.append(row)
            
        data=pd.DataFrame(data).astype('float')
        Y_pred = model.predict(data)
        count_1=len(Y_pred[Y_pred==1])
        count_2=len(Y_pred[Y_pred==2])
        count_3=len(Y_pred[Y_pred==3])
        count_4=len(Y_pred[Y_pred==4])
        count_5=len(Y_pred[Y_pred==5])
        
        safe=[]
        unsafe=[]
        for i in Y_pred:
            if i<5:
                unsafe.append(i)
            else:
                safe.append(i)
        s=len(safe)
        us=len(unsafe)
        good_driving=int((len(safe)/(len(safe)+len(unsafe))*100))
        bad_driving=100-int((len(safe)/(len(safe)+len(unsafe))*100))
                
        per_safe=int((len(safe)/(len(safe)+len(unsafe))*100))
        if per_safe in range(0,30):
            a="Poor Driving ! NO discount for this month"
        elif(per_safe in range(30,60)):
            a="Average Driving ! You will get 5 % discount"
        elif(per_safe in range(60,80)):
            a="Good Driving ! You will get 10 % discount"
        else:
            a="Excellent driving ! You will get 20 % discount"
            
            
        #visualizations
            
        graph = pygal.Pie(half_pie=True)
        graph.title = '% of Good driving to Bad driving'
        graph.add('Good driving',good_driving)
        graph.add('bad_driving',bad_driving)
        graph_data = graph.render_data_uri()
        
        
        graph1 = pygal.Bar()
        graph1.title = 'Count of each type of driving '
        graph1.add('Sudden Acceleration ',count_1)
        graph1.add('Sudden Right Turn ',count_2)
        graph1.add('Sudden Left Turn ',count_3)
        graph1.add('Sudden Brake',count_4)
        graph1.add('Good Driving',count_5)
        graph1_data = graph1.render_data_uri()
        
            
        return render_template('data.html',safe='No of safe driving :{}'.format(s),
                               unsafe='No of Unsafe driving :{}'.format(us),output='{}'.format(a)
                               ,graph_data=graph_data,graph1_data=graph1_data)
            
        
        
    

@app.route('/predict_i',methods=['GET','POST'])
def predict_i():
    int_features = [float(x) for x in request.form.values()]
    final_features = [np.array(int_features)]
    print(final_features)
    Y_pred = model.predict(final_features)
    safe=[]
    unsafe=[]
    for i in Y_pred:
        if i<5:
            unsafe.append(i)
        else:
            safe.append(i)
    s=len(safe)
    us=len(unsafe)
            
    per_safe=int((len(safe)/(len(safe)+len(unsafe))*100))
    if per_safe in range(0,30):
        a="Poor Driving ! NO discount for this month"
    elif(per_safe in range(30,60)):
        a="Average Driving ! You will get 5 % discount"
    elif(per_safe in range(60,80)):
        a="Good Driving ! You will get 10 % discount"
    else:
        a="Excellent driving ! You will get 20 % discount"
        
    return render_template('index.html',safe='No of safe driving :{}'.format(s),
                           unsafe='No of Unsafe driving :{}'.format(us),output='{}'.format(a))


if __name__ == "__main__":
    app.run()





