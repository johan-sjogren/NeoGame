import requests

# Test GET
response = requests.get(
    'http://127.0.0.1:5000/ai/game/v1.0')

# Check speed and response
assert response.status_code in [200], \
    'GET responding with error' + str(response.status_code)
assert response.elapsed.total_seconds() < 0.3, \
    'GET Response is slower than 0.3 s'
try:
    response.json()
except:
    print("Not JSON")

# Test POST for all given models plus default
headers = {
    'Content-Type': 'application/json',
}

# Loop over all models given by GET plus ''
for models in response.json()['Available models']+['']:
    data = '{"opponent_name":"'+models+'"}'
    # print(data)
    response = requests.post('http://127.0.0.1:5000/ai/game/v1.0',
                             data=data, headers=headers)
    # Check response and speed
    assert response.status_code in [200], \
        'POST responding with error: ' + str(response.status_code)
    assert response.elapsed.total_seconds() < 0.3, \
        'POST Response is slower than 0.3 s'

    resp_json = response.json()
    # try:
    #     print(resp_json)
    # except:
    #     print("Did not return in JSON-format")
    # Test that the given model is returned
    if models == "":
        assert resp_json['opponent_name'] == "Default"
    else:
        assert resp_json['opponent_name'] == models

    # Check that the response is as expected
    assert all(isinstance(x, int) for x in resp_json['opponent_action'])
    assert all(x == 0 or x == 1 for x in resp_json['opponent_action'])
    assert all(isinstance(x, int) for x in resp_json['opponent_hand'])
    assert all(isinstance(x, int) for x in resp_json['opponent_table'])
    assert all(isinstance(x, int) for x in resp_json['player_hand'])
    assert all(isinstance(x, int) for x in resp_json['player_table'])
    assert isinstance(resp_json['version'], str)
print('All tests passed')
