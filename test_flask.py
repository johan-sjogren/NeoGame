from run_flask import app
import unittest


class FlaskTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        # creates a test client
        self.app = app.test_client()
        # propagate the exceptions to the test client
        self.app.testing = True

    def tearDown(self):
        # Not neccessary
        pass

    def test_home_status_code(self):
        # sends HTTP GET request to the application
        # on the specified path
        path = '/'
        result = self.app.get(path)
        # assert the status code of the response
        self.assertEqual(result.status_code, 200,
                         msg='GET on ' + path + ' responding with error' +
                             str(result.status_code))

    def test_get_data(self):
        # sends HTTP GET request to the application
        # on the specified path
        path = '/ai/game/v1.0'
        result = self.app.get(path)
        # assert the status code of the response
        self.assertEqual(result.status_code, 200,
                         msg='GET on ' + path + ' responding with error' +
                             str(result.status_code))
        # Is it json
        self.assertTrue(result.is_json, msg='Result is not a json object')
        self.assertIsInstance(result.get_json()['opponents'], list,
                              msg='Response not returning a list as expected')
        self.assertTrue(all(isinstance(x, str)
                            for x in result.get_json()['opponents']))
        return result.get_json()['opponents']

    def test_api(self):
        path = '/ai/game/v1.0'
        results = []
        # Run the tests for post and get a few times
        iterations = 100
        for _ in range(iterations):
            models = self.test_get_data()
            for model in models + ['']:
                results.append(self._post_test(path, model=model))

        # Check that shuffleing is being done.
        for cardlist in ['opponent_action', 'opponent_hand', 'opponent_table',
                         'player_hand', 'player_table']:
            prev = None
            tot = 0
            for x in results:
                if prev is not None:
                    tot += 1 if x[cardlist] == prev else 0
                prev = x[cardlist]
            # TODO: This limit should depend upon the lenght of the lists and 
            # the range of numbers included
            self.assertLess(tot, int(iterations/2))

    def _post_test(self, path, model=''):
        data = {"opponent_name": model}
        result = self.app.post(path, json=data)
        # assert the status code of the response
        self.assertEqual(result.status_code, 200,
                         msg='POST on ' + path + ' responding with error ' +
                             str(result.status_code))
        # Is it json
        self.assertTrue(result.is_json, msg='Result is not a json object')

        # Test that all the hands only contain expected integers
        for cardlist in ['opponent_action', 'opponent_hand', 'opponent_table',
                         'player_hand', 'player_table']:
            self.assertTrue(all(isinstance(x, int)
                                for x in result.get_json()[cardlist]),
                            msg='Everything in ' + cardlist + ' must be' +
                                ' integer instead got: ' +
                                str(result.get_json()[cardlist]))
            self.assertTrue(all(x in [0, 1, 2, 3, 4]
                                for x in result.get_json()[cardlist]),
                            msg='Unexpected number in ' + cardlist + ': ' +
                                str(result.get_json()[cardlist]))

        # Test that opponent action is a 0-1 boolean array
        self.assertTrue(all(x == 0 or x == 1
                            for x in result.get_json()['opponent_action']),
                        msg='Opponent action should only contain 1s and 0s' +
                            ' but got ' +
                            str(result.get_json()['opponent_action']))

        # Check that the version is a string
        self.assertTrue(isinstance(result.get_json()['version'], str),
                        msg='version should be a string')
        return result.get_json()


if __name__ == '__main__':
    unittest.main()
