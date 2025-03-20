import unittest
from unittest.mock import patch, Mock
from apparatusai.client import ApparatusAI

class TestApparatusAI(unittest.TestCase):
    def setUp(self):
        self.api = ApparatusAI("apai_kf963a9c824e86e8e05861768")

    @patch('apparatusai.client.requests.get')
    def test_get_user_info(self, mock_get):
        mock_response = Mock()
        mock_response.json.return_value = {"user": "info"}
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        response = self.api.get_user_info()
        self.assertEqual(response, {"user": "info"})
        mock_get.assert_called_with(
            'https://app.apparatusai.space/api/user/info',
            headers={'Authorization': 'Bearer apai_test_api_token'}
        )

    @patch('apparatusai.client.requests.post')
    def test_forecast(self, mock_post):
        mock_response = Mock()
        mock_response.json.return_value = {"forecast": "data"}
        mock_response.raise_for_status = Mock()
        mock_post.return_value = mock_response

        data = {"revenue": [10000, 12000, 15000]}
        response = self.api.forecast(data)
        self.assertEqual(response, {"forecast": "data"})
        mock_post.assert_called_with(
            'https://app.apparatusai.space/api/forecast',
            headers={
                'Authorization': 'Bearer apai_test_api_token',
                'Content-Type': 'application/json'
            },
            json=data
        )

    @patch('apparatusai.client.requests.post')
    def test_analyze_social_trends(self, mock_post):
        mock_response = Mock()
        mock_response.json.return_value = {"trends": "data"}
        mock_response.raise_for_status = Mock()
        mock_post.return_value = mock_response

        params = {"keyword": "AI Trends"}
        response = self.api.analyze_social_trends(params)
        self.assertEqual(response, {"trends": "data"})
        mock_post.assert_called_with(
            'https://app.apparatusai.space/api/social-analysis',
            headers={
                'Authorization': 'Bearer apai_test_api_token',
                'Content-Type': 'application/json'
            },
            json=params
        )

if __name__ == "__main__":
    unittest.main()

