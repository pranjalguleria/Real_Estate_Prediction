from flask import * 
import pandas as pd
import numpy as np
from datetime import datetime 
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.model_selection import ShuffleSplit
from sklearn.model_selection import cross_val_score
import sqlite3
import requests
from bs4 import BeautifulSoup
from sklearn.metrics import r2_score


# create object of Flask class named as app
app = Flask(__name__)


file ="https://raw.githubusercontent.com/sarwansingh/Python/master/ClassExamples/data/Bengaluru_House_Data_clean.csv"
df = pd.read_csv(file)
X = df.drop(['Unnamed: 0' ,'price'], axis='columns')
Y = df.price

lrmodel = LinearRegression()
lrmodel.fit(X,Y)



def predictprice(location, sqft, bath, bhk):
    loc_index = np.where(X.columns == location)[0][0]
    x = np.zeros(len(X.columns))
    x[0] = sqft
    x[1] = bath
    x[2] = bhk
    if loc_index >= 0: 
        x[loc_index] = 1
    return lrmodel.predict([x])[0]
  


# home page
@app.route('/')
def home():
  return render_template('home.html')

#login to access website
@app.route('/fdata', methods = ['POST'])
def rdata():
  email = request.form['email']
  passwrd = request.form['pwd']
  
  if( email=='2002563.cse.cec@cgc.edu.in' and passwrd== '2002563'):
    return render_template('a.html', msg = "Welcome  !")
  else :
   return render_template('home.html') +"\nSorry, Email/Password is incorrect ! "
  #return "Sorry, Email/Password is incorrect !"
  #return email + passwrd 
  
#about page
@app.route('/b')
def about():
  return render_template('about.html')
  
#prediction dage
@app.route('/c')   #/sform
def evaluate():
  return render_template('evaluate.html', locations = df.columns[5:])   #data = df

#details to predict
@app.route('/pdata', methods=['GET', 'POST'])
def pdata():
    loc = request.form.get("locationSelect")
    bath = (request.form.get("bathrooms"))  
    bhk = (request.form.get("bedrooms"))     
    sqft = (request.form.get("sq_ft"))      
    
    # Print the form values for debugging
    print(loc)
    print(sqft)
    print(bhk)
    print(bath)
    
    # Ensure consistency with the parameter order in the predictprice function
    pp = predictprice(loc, sqft, bath, bhk).round(3)
    
    # Define the feature vector x
    loc_index = np.where(X.columns == loc)[0][0]
    x = np.zeros(len(X.columns))
    x[0] = bhk
    x[1] = bath
    x[2] = sqft
    if loc_index >= 0: 
        x[loc_index] = 1
    
    # Make prediction using lrmodel
    prediction = lrmodel.predict([x])[0]
    
    # Debug statements
    input_features = (loc, sqft, bath, bhk)
    debug_prediction = prediction
    
    print(pp)
    
    return render_template('pdata.html', pprice=pp, loc=loc, sqft=sqft, bhk=bhk, bath=bath,
                           input_features=input_features, debug_prediction=debug_prediction)


#+"\nLocation Selected : "  +loc+"\nSquare Feet : " + sqft+"\nNumber of bedrroms: " + bhk+"\nNumber of bathrooms : " + bath 

#contact details
@app.route('/information')
def contact():
  return render_template('contact.html')

#visualizing data
@app.route('/datavisual')
def visual():
  return render_template('datavisual.html')

#news section
@app.route('/news')
def news():
  return render_template('news.html')

@app.route('/latesttrends')
def ltrends():
  api_key = 'e72839693cfb4fcabbe6d282cdb10382'
  url = 'https://newsapi.org/v2/everything?q=karnataka%20real%20estate&apiKey=' + api_key
  response = requests.get(url)
  data = response.json()
  articles = data.get('articles', [])
  return render_template('l_trends.html', articles=articles)

@app.route('/govtnews')
def govtnews(): 
  api_key = 'e72839693cfb4fcabbe6d282cdb10382'
  url = 'https://newsapi.org/v2/everything?q=karnataka%20real%20estate&apiKey=' + api_key
  response = requests.get(url)
  data = response.json()
  articles = data.get('articles', [])
  return render_template('govtnews.html', articles=articles)

@app.route('/marketanalysis')
def marketnews():
  api_key = 'e72839693cfb4fcabbe6d282cdb10382'
  url = 'https://newsapi.org/v2/everything?q=india%20market%20analysis+Market+Property&language=en&apiKey=' + api_key
  response = requests.get(url)
  data = response.json()
  articles = data.get('articles', [])
  return render_template('marketnews.html', articles=articles)

@app.route('/expertinsights')
def expertnews():
  return render_template('expertnews.html')

#faq page
@app.route('/questions')
def faq():
  return render_template('faq.html')

#Image Gallery
@app.route('/gallery')
def gallery():
  return render_template('gallery.html')


#instantiate / call the run method of app object
if __name__ =='__main__':
  app.run(debug = True)
  