from flask import Flask, render_template, jsonify, request
import requests
from bs4 import BeautifulSoup
from pandas import DataFrame
import math
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    weight = 130
    lift = 205
    if request.method == 'POST':
        # Get the number from the form
        weight = int(request.form.get('user_weight'))
        lift = int(request.form.get('user_lift'))

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
        data = {}
        for i in range(1,len(m[0])): data[m[0][i]] = []
        for j in range(1,len(m[0])):
            for i in range(1,len(m)): data[m[0][j]].append(int(m[i][j]))
        
        weight -= weight%10
        weight_class = data[str(weight)]
        res = 1
        for i in range(len(weight_class)):
            if lift < weight_class[i]: break
            res += 1

    
    
    
    return render_template('index.html', result=res)

if __name__ == '__main__':
    app.run(debug=True)
