import pytest
from rest_framework.reverse import reverse


class TestPerevalsEndpoint:
    #  This tests is more like for debugging purposes
    url = reverse('passes')

    @pytest.mark.django_db
    def test_pereval_endpoint_post(self, api_client, test_post_values):
        response = api_client.post(self.url, test_post_values, format="json")
        response_data = response.data
        print(response_data)

    @pytest.mark.django_db
    def test_pereval_endpoint_post_key_error(self, api_client, test_post_values_without_secondary_info):
        response = api_client.post(self.url, test_post_values_without_secondary_info, format="json")
        response_data = response.data
        print(response_data)


