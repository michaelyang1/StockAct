import requests
import pandas as pd
url = "https://api.quiverquant.com/beta/live/housetrading"
headers = {'accept': 'application/json',
'X-CSRFToken': 'TyTJwjuEC7VV7mOqZ622haRaaUr0x0Ng4nrwSRFKQs7vdoBcJlK9qjAS69ghzhFu',
'Authorization': 'Token 591c8fca810b40d0893aa0276056760ed097e082'}
r = requests.get(url, headers=headers)
data = r.content

print(len(data))
print(data[:100])

