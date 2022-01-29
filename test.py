

from bs4 import BeautifulSoup # BeautifulSoup is in bs4 package 


import requests

url = "https://scrapingant.p.rapidapi.com/post"

payload = "{\n    \"cookies\": \"cookie_name_1=cookie_value_1;cookie_name_2=cookie_value_2\",\n    \"return_text\": false,\n    \"url\": \"https://app.capitoltrades.com/politician/491\"\n}"
headers = {
    'content-type': "application/json",
    'x-rapidapi-host': "scrapingant.p.rapidapi.com",
    'x-rapidapi-key': "49a69bc058msh832d1a6394dc332p11d3b1jsna43e1efd6007"
    }

response = requests.request("POST", url, data=payload, headers=headers)

# print(response.text)

text = response.text

start = text.find('<p-table')
stop = text.find('</p-table')+10

print(start)
print(stop)

table = text[start:stop]

print(table)
print("\n\n\n")
table = BeautifulSoup(table)
print(table.get_text())