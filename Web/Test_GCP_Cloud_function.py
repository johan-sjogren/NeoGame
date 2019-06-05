import requests

headers = {
    'Content-Type': 'application/json',
}

print('Testing the GCP Cloud function API')
for x in ['"Random"', '"Greedy"','', '"greedy"']:
        data = '{"model":'+x+'}' 
        print(data)
        response = requests.post('https://europe-west1-neogamebackend.cloudfunctions.net/NeoGameGCP', headers=headers, data=data)
        print(response)
        print('Response time: ', response.elapsed.total_seconds())
        try:
                print(response.json())
        except:
                print("Not JSON")

''' Curl equivalent
    curl -X POST "https://europe-west1-neogamebackend.cloudfunctions.net/NeoGameGCP" -H "Content-Type:application/json" --data '{"model":"Random"}'
 '''
