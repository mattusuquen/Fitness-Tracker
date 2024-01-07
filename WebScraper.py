from flask import Flask, render_template, jsonify, request
import requests
from bs4 import BeautifulSoup
from pandas import DataFrame
import math
import numpy as np
app = Flask(__name__, static_url_path='/static')

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    weight = 130
    lift = 205
    #reps = 1
    if request.method == 'POST':
        # Get the number from the form
        weight = int(request.form.get('user_weight'))
        lift = int(request.form.get('user_lift'))
        #reps = int(request.form.get('user_reps'))

    url = 'https://strengthlevel.com/strength-standards/bench-press'
    response = requests.get(url)
    if response.status_code == 200:

        soup = BeautifulSoup(response.text, 'html.parser')
        tables = soup.find_all('table')
        #table = tables[7] #FEMALE STANDARD BY BW
        #table = tables[8] #FEMALE STANDARD BY AGE
        table = tables[2] #MALE STANDARD BY BW
        #table = tables[3] #MALE STANDARD BY AGE
        m = [[] for i in range(6)]
        i = 0
        for row in table.find_all('tr'):
            columns = row.find_all(['td', 'th'])
            for column in columns: 
                m[i%6].append(column.get_text(strip=True))
                i += 1
        for i in range(len(m)): m[i] = m[i][1:]
        #print(m)
        
        data = []
        output = []

        for j in range(len(m[0])):
            for i in range(1,len(m)):
                data.append([1, int(m[0][j]),int(m[i][j])])
                output.append(i)
        #constant,weight, lift
        x = np.array(data)
        y = np.array(output)
        
        input = np.array([1,weight,lift])
        w = np.linalg.lstsq(x,y,rcond=None)[0]

    
    return render_template('index.html', result=str(round(np.dot(input,w),1))+'/5.0')

if __name__ == '__main__':
    app.run(debug=True)
