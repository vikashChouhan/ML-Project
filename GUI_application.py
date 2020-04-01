"""
This file contains the UI interface for running the ML models that are trained
on Soil dataset.

It contains the GUI interface that takes inputs from user and predicts the 
vegeration cover using various models.


@author: Vikash Chouhan
"""

################
#
#   Warning:
#
#   This Application need the 'Model' folder in same dir to work, as it contains the trained
#   Models, changing names of deleting models would not work.
#
###############



# importing necessary files
import tkinter as tk
from sklearn.linear_model import LinearRegression, Lasso, Ridge
from sklearn.svm import SVR
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.neural_network import MLPRegressor
import numpy as np
import pickle

#models
models = ['Decision Tree Regressor', 'Random Forest Regressor', 'Neural Network', 
          'SVR (Linear)', 'SVR (poly)', 'Linear Model', 'Ridge', 'Lasso']

#attributes and their units
attributes = ['NO3','NH4','P','K','SO4','B','Organic Matter','pH','Zn','Cu','Fe','Ca','Mg','Na']
units = ['ppm','ppm','ppm','ppm','ppm','ppm',"%age",'pH','ppm','ppm','ppm','meq/100g','meq/100g','meq/100g']

################
#
#   predict function to call
#
###############
def predictFun(attribute_values, model_idx, result_text):
    global models 
    
    X = np.zeros((1,len(attribute_values)))
    try:
        for i in range(len(attribute_values)):
            X[0][i] = np.float32(attribute_values[i].get())
            if(X[0][i]<0):
                raise 1
        
        
        model = pickle.load(open('Models\\'+models[model_idx.get()],'rb'))
        
        X = (X-X.min())/(X.max() - X.min())
        y_pred = model.predict(X)
        if(y_pred[0]>0 and y_pred[0]<1):
            result_text.set(y_pred[0])
        else:
            tk.messagebox.showwarning(title='Warning',message='Not valid input for soil.')
    except:
        tk.messagebox.showerror(title='Error',message='Wrong Input! Make sure you enter correct values and at least a model is selected.')
   
################
#
#create main window
#
############### 
mainWindow = tk.Tk(className='Soil Testing')
mainWindow.geometry('750x600')
mainWindow.resizable(width=False, height=False)


################
#
#heading 
#
###############
heading = tk.Label(mainWindow,text="Automatic Soil Testing Using AI")
heading.config(font=('Aerial',16))
heading.place(x=170,y=10)


################
#
#warning text
#
###############
warning_text = tk.Label(mainWindow,text="Please Enter the decimal values only")
warning_text.config(font=('Aerial',9))
warning_text.place(x=20,y=70)



################
#
# adding input boxes
#
###############
labels = list()
label_val = list()
init_y = 100
for i in range(len(attributes)//2):

    label = tk.Label(mainWindow,text= attributes[i] + ' ('+units[i]+')')
    label.config(font=('Times New Roman',12))
    label.place(x=20, y=init_y)
    
    label_val.append(tk.StringVar())
    textBox = tk.Entry(mainWindow, textvariable=label_val[-1])
    textBox.place(x=20, y=init_y+30)
    
    labels.append(label)
    init_y+=70

init_y = 100
for i in range(len(attributes)//2,len(attributes)):

    label = tk.Label(mainWindow,text= attributes[i] + ' ('+units[i]+')')
    label.config(font=('Times New Roman',12))
    label.place(x=300, y=init_y)
    
    label_val.append(tk.StringVar())
    textBox = tk.Entry(mainWindow, textvariable=label_val[-1])
    textBox.place(x=300, y=init_y+30)
    
    init_y+=70

################
#
# add model options to screen
#
###############
init_y = 100
radio_variable = tk.IntVar(mainWindow,i)


for i in range(len(models)):
    
    radio_btn = tk.Radiobutton(mainWindow, text=models[i], variable=radio_variable, value=i)
    radio_btn.place(x=520, y=init_y)
    
    init_y+=30


result_text = tk.Label(mainWindow,text='Vegetation Cover')
result_text.place(x=520, y=400)

result_variable = tk.StringVar()
result = tk.Entry(mainWindow,textvariable=result_variable )
result.config(state=tk.DISABLED)
result.place(x=520, y=430)

predict = tk.Button(mainWindow, text='Predict', 
                    width=19,command=lambda: predictFun(label_val,radio_variable,result_variable))
predict.place(x=520,y=460)


################
#
#loop for main Window Screen
#
###############
mainWindow.mainloop()

