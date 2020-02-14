from run_flask import app
from collections import Counter
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
        # Run the tests for post
        iterations = 100  # iterations per opponent model
        for _ in range(iterations):
            models = self.test_get_data()
            for model in models + ['']:
                results.append(self._post_test(path, model=model))
        num_results = len(results)

        self.assertTrue(num_results > 350,
                        msg='Test based on {} samples'.format(num_results) +
                        ' , review the number of iterations and models')

        """ Check that cards are shuffled i.e. that the number of
        different combinations are at least within the right ballpark"""
        def get_combination_counter(results, card_str):
            combination_list = []
            for x in results:
                combination_list.append(x[card_str])
            return Counter(str(x) for x in combination_list)

        count = get_combination_counter(results, 'opponent_action')
        # Opponent action has 10 states (pick two places out of five)
        self.assertTrue(len(count) > 9,
                        msg='Got {} different states,'.format(len(count)) +
                        ' expected 10 for the standard game implementation')
        # Checking twice the expected mean
        self.assertTrue(all([x < 80 for x in count.values()]),
                        msg='Got too many examples of some states ' +
                        '{}'.format(count.most_common(4)))

        # Table has 25 states (5x5)
        for table in ['opponent_table', 'player_table']:
            count = get_combination_counter(results, table)
            self.assertTrue(len(count) > 24,
                            msg='Got {} different states,'.format(len(count)) +
                            ' expected 25 for the standard game')
        # Checking twice the expected mean
            self.assertTrue(all([x < 32 for x in count.values()]),
                            msg='Got too many examples of some states ' +
                            '{}'.format(count.most_common(4)))

        # Hands has many more states (5^5)
        for hand in ['opponent_hand', 'player_hand']:
            count = get_combination_counter(results, hand)
            self.assertTrue(len(count) > num_results-int(num_results/4),
                            msg='Got {} different states,'.format(len(count)) +
                            ' expect a number close to number of ' +
                            'results {} the standard game'.format(num_results))
            self.assertTrue(all([x < 5 for x in count.values()]),
                            msg='Got too many examples of some states ' +
                            '{}'.format(count.most_common(4)))

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
