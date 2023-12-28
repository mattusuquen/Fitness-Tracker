import requests
from bs4 import BeautifulSoup
from pandas import DataFrame

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
    for category in m:
        data[category[0]] = []
        for i in range(1,len(category)): data[category[0]].append(category[i])

    df = DataFrame(data)
    print(df)
    df.to_excel('data.xlsx', index=False)
    
else: print(f"Failed to retrieve the webpage. Status code: {response.status_code}")