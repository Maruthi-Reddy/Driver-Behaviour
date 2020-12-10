import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import pickle
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV



# Sudden Acceleration (Class Label: 1)
# Sudden Right Turn (Class Label: 2)
# Sudden Left Turn (Class Label: 3)
# Sudden Break (Class Label: 4)
# Good driving (class Label :5)

df=pd.read_csv('sensor_raw.csv')
df.head()

from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(df.iloc[:,1:])
Y_train=df.iloc[:,0]
X_train_scaled,X_test_scaled,Y_train,Y_test=train_test_split(X_train_scaled,Y_train,test_size=0.30,random_state=44)

params_grid={'C':[0.1,1,10,100,1000],'gamma':[1,0.1,0.01,0.001,0.0001]}
svm_model = GridSearchCV(SVC(), params_grid, cv=5)
svm_model.fit(X_train_scaled, Y_train)

print('Best score for training data:', svm_model.best_score_,"\n") 

# View the best parameters for the model found using grid search
print('Best C:',svm_model.best_estimator_.C,"\n") 
print('Best Kernel:',svm_model.best_estimator_.kernel,"\n")
print('Best Gamma:',svm_model.best_estimator_.gamma,"\n")

final_model = svm_model.best_estimator_
print("Training set score for SVM: %f" % final_model.score(X_train_scaled , Y_train))
print("Testing  set score for SVM: %f" % final_model.score(X_test_scaled  , Y_test ))



pickle.dump(final_model, open('model.pickle','wb'))
model = pickle.load(open('model.pickle','rb'))


"""def predict(data):
    Y_pred = final_model.predict(data)
    safe=[]
    unsafe=[]
    for i in Y_pred:
        if i<5:
            unsafe.append(i)
        else:
            safe.append(i)
    print("No of safe driving :",len(safe))
    print("No of unsafe driving :",len(unsafe))
            
    per_safe=int((len(safe)/(len(safe)+len(unsafe))*100))
    if per_safe in range(0,30):
        print("Poor Driving ! NO discount for this month")
    elif(per_safe in range(30,60)):
        print("Average Driving ! You will get 5 % discount")
    elif(per_safe in range(60,80)):
        print("Good Driving ! You will get 10 % discount")
    else:
        print("Excellent driving ! You will get 20 % discount")"""

Y_pred=model.predict(pd.read_csv('test.csv'))
Y_pred




