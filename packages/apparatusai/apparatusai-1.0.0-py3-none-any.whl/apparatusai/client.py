import requests

class ApparatusAI:
    def __init__(self, api_token):
        if not api_token.startswith("apai_"):
            raise ValueError("Invalid API token. Ensure it starts with 'apai_'.")
        self.api_token = api_token
        self.base_url = "https://app.apparatusai.space"

    def _request(self, endpoint, method="GET", data=None):
        url = f"{self.base_url}{endpoint}"
        headers = {"Authorization": f"Bearer {self.api_token}"}
        if method == "POST":
            headers["Content-Type"] = "application/json"
            response = requests.post(url, headers=headers, json=data)
        else:
            response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()

    def get_user_info(self):
        return self._request("/api/user/info")

    def forecast(self, data):
        return self._request("/api/forecast", method="POST", data=data)

    def analyze_social_trends(self, params):
        return self._request("/api/social-analysis", method="POST", data=params)

