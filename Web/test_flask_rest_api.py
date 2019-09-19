import requests

# Run the test a couple of times
for _ in range(100):
    # Test GET
    response = requests.get(
        'http://127.0.0.1:5000/ai/game/v1.0')

    # Check speed and response
    assert response.status_code in [200], \
        'GET responding with error' + str(response.status_code)
    assert response.elapsed.total_seconds() < 0.3, \
        'GET Response is slower than 0.3 s'

    resp_json = response.json()
    assert isinstance(resp_json['opponents'], list), \
        'Response not returning a list as expected'

    for opp in resp_json['opponents']:
        assert isinstance(opp, str), 'An object in the list is not a string'

    headers = {
        'Content-Type': 'application/json',
    }

    # Test POST for all given models plus default
    # Loop over all models given by GET plus ''
    for models in response.json()['opponents']+['']:
        data = '{"opponent_name":"'+models+'"}'
        response = requests.post('http://127.0.0.1:5000/ai/game/v1.0',
                                 data=data, headers=headers)
        # Check response and speed
        assert response.status_code in [200], \
            'POST responding with error: ' + str(response.status_code)
        assert response.elapsed.total_seconds() < 0.3, \
            'POST Response is slower than 0.3 s'

        resp_json = response.json()

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
