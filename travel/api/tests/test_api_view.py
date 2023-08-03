import pytest
from rest_framework.reverse import reverse


class TestPerevalsEndpoint:
    url = reverse('passes')

    @pytest.mark.django_db
    def test_pereval_endpoint_post(self, api_client, test_post_values):
        response = api_client.post(self.url, test_post_values, format="json")
        response_data = response.data
        print(response_data)
