from rest_framework.test import APIClient
from organization.models import Organization
from organization.tests import base_test


class OrganizationCreateTestCase(base_test.NewUserTestCase):
    """
    Organization Create API Test Case
    """

    def setUp(self) -> None:
        super().setUp()

        self.client = APIClient()

        login_response = self.client.post('/api/v1/users/login/', {
            'username': self.username,
            'password': self.password
        }, format='json')

        access_token = login_response.json()['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + access_token)

    def test_organization_create_api(self):
        create_organization = self.client.post('/api/v1/organizations/', {
            'name': 'Apple',
            'registration_code': '101010101',
            'established_on': '1976-04-01',
        }, format='json')

        self.assertEquals(create_organization.status_code, 201)
        self.assertTrue('Apple' in create_organization.json()['data']['name'])
        self.assertTrue('101010101' in create_organization.json()['data']['registration_code'])
        self.assertTrue('1976-04-01' in create_organization.json()['data']['established_on'])

    def tearDown(self) -> None:
        self.client.logout()
        Organization.objects.filter().delete()
        super().tearDown()


class OrganizationListingTestCase(base_test.NewUserTestCase):
    """
    Organization Listing API Test Case
    """

    def setUp(self) -> None:
        super().setUp()

        self.client = APIClient()

        login_response = self.client.post('/api/v1/users/login/', {
            'username': self.username,
            'password': self.password
        }, format='json')

        access_token = login_response.json()['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + access_token)

        # Create a new Organization
        self.organization = Organization.objects.create(
            name='Robert Bosch GmbH',
            established_on='1886-11-15',
            registration_code='112211'
        )

    def test_organization_listing_api(self):
        list_organizations = self.client.get('/api/v1/organizations/', format='json')

        self.assertEquals(list_organizations.status_code, 200)
        self.assertTrue('Robert Bosch GmbH' in list_organizations.json()['results'][0]['name'])

    def tearDown(self) -> None:
        self.client.logout()
        Organization.objects.filter().delete()
        super().tearDown()
