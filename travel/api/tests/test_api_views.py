import pytest
from rest_framework.reverse import reverse
from rest_framework import status


class TestPerevalsEndpoint:
    url = reverse('passes_add')

    @pytest.mark.django_db
    def test_post_pereval(self, api_client, test_post_values):
        """
        Testing: Usual post requests with right parameters
        Expected: Success status and message
        """
        response = api_client.post(self.url, test_post_values, format="json")
        print(response.data)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['message'] == 'success'

    @pytest.mark.django_db
    def test_post_key_error(self, api_client):
        """
        Testing: Throws out exception if missing main parameters
        Expected: Error message with key error
        """
        values_without_secondary_info = {
            "beauty_title": "пер. ",
            "title": "Прокова",
            "other_titles": "Триев",
            "connect": "",
            "add_time": "2021-09-22 13:18:13",
        }
        response = api_client.post(self.url, values_without_secondary_info)
        print(response.data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "Key error" in response.data['message']


class TestPerevalDetailEndpoint:
    url = reverse('pass_detail', kwargs={'pk': 1})
    FAIL_STATE = 0
    SUCCESS_STATE = 1

    @pytest.mark.django_db
    def test_get(self, api_client, test_post_values):
        """
        Testing: Usual get request with correct values
        Expected: sent values == saved values
        """
        response = api_client.get(self.url)
        response_data = response.data
        assert response_data['beauty_title'] == test_post_values['beauty_title']
        assert response_data['user']['email'] == test_post_values['user']['email']
        assert response_data['coords']['latitude'] == test_post_values['coords']['latitude']
        assert response_data['level']['summer'] == test_post_values['level']['summer']
        assert response_data['images'][0]['title'] == test_post_values['images'][0]['title']

    @pytest.mark.django_db
    def test_patch_wrong_type(self, api_client, test_post_values):
        """
        Testing: Throws out exception if wrong type
        Expected: Error message with invalid
        """
        wrong_type = {
            "coords": {"longitude": "test"}
        }

        response = api_client.patch(self.url, wrong_type, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['state'] == self.FAIL_STATE
        assert "invalid" in response.data['message']

    @pytest.mark.django_db
    def test_patch_no_id_for_image(self, api_client):
        """
        Testing: Throws out exception if no id entered for image
        Expected: Error message with key error
        """
        no_id_images = {
            "images": [{"title": "test_change"}]
        }

        response = api_client.patch(self.url, no_id_images, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['state'] == self.FAIL_STATE
        assert "Key error, enter" in response.data["message"]

    @pytest.mark.django_db
    def test_patch_change_coords_info(self, api_client):
        """
        Testing: Partial update for coords
        Expected: Message with success and correct changes
        """
        partial_coords = {
            "coords": {"longitude": "18.1525"}
        }
        response = api_client.patch(self.url, partial_coords, format="json")
        assert response.status_code == status.HTTP_200_OK
        assert response.data['state'] == self.SUCCESS_STATE

        check_if_changed_response = api_client.get(self.url)
        assert check_if_changed_response.data['coords']['longitude'] == partial_coords['coords']['longitude']

    @pytest.mark.django_db
    def test_patch_change_level_info(self, api_client):
        """
        Testing: Partial update for level
        Expected: Message with success and correct changes
        """
        partial_level = {
            "level": {"winter": "2A"}
        }
        response = api_client.patch(self.url, partial_level, format="json")

        assert response.status_code == status.HTTP_200_OK
        assert response.data['state'] == self.SUCCESS_STATE

        check_if_changed_response = api_client.get(self.url)
        assert check_if_changed_response.data['level']['winter'] == partial_level['level']['winter']

    @pytest.mark.django_db
    def test_patch_change_images_info(self, api_client):
        """
        Testing: Partial update for images
        Expected: Message with success and correct changes
        """
        partial_images = {
            "images": [{"id": 1,
                        "title": "test_change"}]
        }
        response = api_client.patch(self.url, partial_images, format="json")
        assert response.status_code == status.HTTP_200_OK
        assert response.data['state'] == self.SUCCESS_STATE

        check_if_changed_response = api_client.get(self.url)
        assert check_if_changed_response.data['images'][0]['title'] == partial_images['images'][0]['title']

    @pytest.mark.django_db
    def test_patch_change_status_if_status_is_new(self, api_client):
        """
        Testing: Partial update for status
        Expected: Message with success
        """
        change_status = {
            "status": "accepted"
        }

        response = api_client.patch(self.url, change_status, format="json")
        assert response.status_code == status.HTTP_200_OK
        assert response.data['state'] == self.SUCCESS_STATE

    @pytest.mark.django_db
    def test_patch_change_if_status_is_not_new(self, api_client):
        """
        Testing: Throws out exception if pass status is not new
        Expected: Error message that you cannot change this object
        """
        any_info_to_change = {
            "title": "test_change"
        }
        change_status = {
            "status": "accepted"
        }
        api_client.patch(self.url, change_status, format="json")
        response = api_client.patch(self.url, any_info_to_change, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['state'] == self.FAIL_STATE
        assert "Cannot modify passes that is not new" in response.data['message']


class TestPerevalQueryEndpoint:
    url = reverse('pass_query')

    @pytest.mark.django_db
    def test_get_objects_with_email(self, api_client, test_post_values):
        """
        Testing: Usual get with query parameters
        Expected: Objects with same email
        """
        query = '?user__email=qwerty@mail.ru'
        response = api_client.get(self.url+query)
        assert response.data[0]['user']['email'] == response.data[1]['user']['email']

    @pytest.mark.django_db
    def test_get_objects_with_no_existing_email(self, api_client):
        """
        Testing: Behave if there is no user with email
        Expected: Error message that user is not found
        """
        query = '?user__email=qwe@mail.ru'
        response = api_client.get(self.url + query)
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data['message'] == "User not found"
