import unittest
from unittest.mock import patch

from folio_curl import auth, get_holdings, get_instances, get_items, get_records


class TestAuth(unittest.TestCase):
    def setUp(self):
        # Set up some common variables for testing
        self.url = "https://folio.example.com"
        self.username = "testuser"
        self.password = "testpass"
        self.tenant = "testtenant"

    @patch('requests.post')
    def test_valid_credentials(self, mock_post):
        # Arrange
        # Use the variables from setUp
        # Create a mock response object with a valid token header
        mock_response = unittest.mock.Mock()
        mock_response.headers = {'x-okapi-token': 'valid-token'}
        # Make the mock post function return the mock response object
        mock_post.return_value = mock_response
        # Act
        token = auth(self.url, self.username, self.password, self.tenant)
        # Assert
        self.assertIsNotNone(token)
        self.assertIsInstance(token, str)
        self.assertEqual(token, 'valid-token')
        # Verify that the mock post function was called with the correct arguments
        mock_post.assert_called_once_with(
            f'{self.url}/authn/login',
            headers={
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'X-Okapi-Tenant': self.tenant,
            },
            json={'username': self.username, 'password': self.password},
        )

    @patch('requests.post')
    def test_invalid_credentials(self, mock_post):
        # Arrange
        # Use the variables from setUp but change the password to an invalid one
        invalid_password = "wrongpass"
        # Create a mock response object with no token header
        mock_response = unittest.mock.Mock()
        mock_response.headers = {}
        # Make the mock post function return the mock response object
        mock_post.return_value = mock_response
        # Act
        token = auth(self.url, self.username, invalid_password, self.tenant)
        # Assert
        self.assertIsNone(token)
        # Verify that the mock post function was called with the correct arguments
        mock_post.assert_called_once_with(
            f'{self.url}/authn/login',
            headers={
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'X-Okapi-Tenant': self.tenant,
            },
            json={'username': self.username, 'password': invalid_password},
        )


class TestGetInstances(unittest.TestCase):
    def setUp(self):
        # Set up some common variables for testing
        self.token = "valid-token"
        self.url = "https://folio.example.com"
        self.hrid = "1234567890"
        self.tenant = "testtenant"

    @patch('requests.get')
    def test_valid_hrid(self, mock_get):
        # Arrange
        # Use the variables from setUp
        # Create a mock response object with a valid instance ID
        mock_response = unittest.mock.Mock()
        mock_response.json.return_value = {
            'instances': [{'id': 'instance-id-1'}, {'id': 'instance-id-2'}]
        }
        # Make the mock get function return the mock response object
        mock_get.return_value = mock_response
        # Act
        ids = get_instances(self.token, self.url, self.hrid, self.tenant)
        # Assert
        self.assertIsNotNone(ids)
        self.assertIsInstance(ids, list)
        self.assertEqual(ids, ['instance-id-1', 'instance-id-2'])
        # Verify that the mock get function was called with the correct arguments
        mock_get.assert_called_once_with(
            f'{self.url}/instance-storage/instances',
            headers={
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'X-Okapi-Tenant': self.tenant,
                'X-Okapi-Token': self.token,
            },
            params={'query': f'(hrid=="{self.hrid}" NOT discoverySuppress==true)'},
        )

    @patch('requests.get')
    def test_invalid_hrid(self, mock_get):
        # Arrange
        # Use the variables from setUp but change the hrid to an invalid one
        invalid_hrid = "9999999999"
        # Create a mock response object with an empty instance list
        mock_response = unittest.mock.Mock()
        mock_response.json.return_value = {'instances': []}
        # Make the mock get function return the mock response object
        mock_get.return_value = mock_response
        # Act
        ids = get_instances(self.token, self.url, invalid_hrid, self.tenant)
        # Assert
        self.assertEqual(ids, [])
        # Verify that the mock get function was called with the correct arguments
        mock_get.assert_called_once_with(
            f'{self.url}/instance-storage/instances',
            headers={
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'X-Okapi-Tenant': self.tenant,
                'X-Okapi-Token': self.token,
            },
            params={'query': f'(hrid=="{invalid_hrid}" NOT discoverySuppress==true)'},
        )


class TestGetHoldings(unittest.TestCase):
    def setUp(self):
        # Set up some common variables for testing
        self.token = "valid-token"
        self.url = "https://folio.example.com"
        self.instance_id = "instance-id"
        self.tenant = "testtenant"

    @patch('requests.get')
    def test_valid_instance_id(self, mock_get):
        # Arrange
        # Use the variables from setUp
        # Create a mock response object with a list of holding IDs
        mock_response = unittest.mock.Mock()
        mock_response.json.return_value = {
            'holdingsRecords': [{'id': 'holding-id-1'}, {'id': 'holding-id-2'}]
        }
        # Make the mock get function return the mock response object
        mock_get.return_value = mock_response
        # Act
        id_list = get_holdings(self.token, self.url, self.instance_id, self.tenant)
        # Assert
        self.assertIsNotNone(id_list)
        self.assertIsInstance(id_list, list)
        self.assertEqual(id_list, ['holding-id-1', 'holding-id-2'])
        # Verify that the mock get function was called with the correct arguments
        mock_get.assert_called_once_with(
            f'{self.url}/holdings-storage/holdings',
            headers={
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'X-Okapi-Tenant': self.tenant,
                'X-Okapi-Token': self.token,
            },
            params={
                'query': f'(instanceId=="{self.instance_id}" NOT discoverySuppress==true)'
            },
        )

    @patch('requests.get')
    def test_invalid_instance_id(self, mock_get):
        # Arrange
        # Use the variables from setUp but change the instance_id to an invalid one
        invalid_instance_id = "invalid-id"
        # Create a mock response object with an empty holdings list
        mock_response = unittest.mock.Mock()
        mock_response.json.return_value = {'holdingsRecords': []}
        # Make the mock get function return the mock response object
        mock_get.return_value = mock_response
        # Act
        id_list = get_holdings(self.token, self.url, invalid_instance_id, self.tenant)
        # Assert
        # Expect an empty list instead of None
        self.assertEqual(id_list, [])
        # Verify that the mock get function was called with the correct arguments
        mock_get.assert_called_once_with(
            f'{self.url}/holdings-storage/holdings',
            headers={
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'X-Okapi-Tenant': self.tenant,
                'X-Okapi-Token': self.token,
            },
            params={
                'query': f'(instanceId=="{invalid_instance_id}" NOT discoverySuppress==true)'
            },
        )


class TestGetItems(unittest.TestCase):
    def setUp(self):
        # Set up some common variables for testing
        self.token = "valid-token"
        self.url = "https://folio.example.com"
        self.holding_id = "holding-id"
        self.tenant = "testtenant"

    @patch('requests.get')
    def test_valid_holding_id(self, mock_get):
        # Arrange
        # Use the variables from setUp
        # Create a mock response object with a list of item IDs
        mock_response = unittest.mock.Mock()
        mock_response.json.return_value = {
            'items': [{'id': 'item-id-1'}, {'id': 'item-id-2'}]
        }
        # Make the mock get function return the mock response object
        mock_get.return_value = mock_response
        # Act
        id_list = get_items(self.token, self.url, self.holding_id, self.tenant)
        # Assert
        self.assertIsNotNone(id_list)
        self.assertIsInstance(id_list, list)
        self.assertEqual(id_list, ['item-id-1', 'item-id-2'])
        # Verify that the mock get function was called with the correct arguments
        mock_get.assert_called_once_with(
            f'{self.url}/item-storage/items',
            headers={
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'X-Okapi-Tenant': self.tenant,
                'X-Okapi-Token': self.token,
            },
            params={
                'query': f'(holdingsRecordId=="{self.holding_id}" NOT discoverySuppress==true)'
            },
        )

    @patch('requests.get')
    def test_invalid_holding_id(self, mock_get):
        # Arrange
        # Use the variables from setUp but change the holding_id to an invalid one
        invalid_holding_id = "invalid-id"
        # Create a mock response object with an empty items list
        mock_response = unittest.mock.Mock()
        mock_response.json.return_value = {'items': []}
        # Make the mock get function return the mock response object
        mock_get.return_value = mock_response
        # Act
        id_list = get_items(self.token, self.url, invalid_holding_id, self.tenant)
        # Assert
        # Expect an empty list instead of None
        self.assertEqual(id_list, [])
        # Verify that the mock get function was called with the correct arguments
        mock_get.assert_called_once_with(
            f'{self.url}/item-storage/items',
            headers={
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'X-Okapi-Tenant': self.tenant,
                'X-Okapi-Token': self.token,
            },
            params={
                'query': f'(holdingsRecordId=="{invalid_holding_id}" NOT discoverySuppress==true)'
            },
        )


class TestGetRecords(unittest.TestCase):
    def setUp(self):
        # Set up some common variables for testing
        self.url = "https://folio.example.com"
        self.username = "testuser"
        self.password = "testpass"
        self.tenant = "testtenant"
        self.hrid = "1234567890"

    @patch('folio_curl.get_items')
    @patch('folio_curl.get_holdings')
    @patch('folio_curl.get_instances')
    @patch('folio_curl.auth')
    def test_valid_hrid(
        self, mock_auth, mock_get_instances, mock_get_holdings, mock_get_items
    ):
        # Arrange
        # Use the variables from setUp
        # Create a mock token and lists of item IDs
        mock_token = "valid-token"
        # Make the mock auth function return the mock token
        mock_auth.return_value = mock_token
        # Make the mock get_instances function return a list of instance IDs
        mock_get_instances.return_value = ["instance-id-1", "instance-id-2"]
        # Make the mock get_holdings function return a list of lists of holding IDs
        mock_get_holdings.side_effect = [["holding-id-1"], ["holding-id-2"]]
        # Make the mock get_items function return a list of item IDs for each holding ID
        # Use a loop to generate item IDs dynamically based on the holding ID

        def generate_item_ids(token, url, holding_id, tenant):
            return [f"{holding_id}-item-{i}" for i in range(1, 3)]

        mock_get_items.side_effect = generate_item_ids
        # Act
        with patch('builtins.print') as mock_print:
            id_list = get_records(
                self.url, self.username, self.password, self.tenant, self.hrid
            )
            # Assert
            self.assertIsNotNone(id_list)
            self.assertIsInstance(id_list, list)
            expected_result = [
                ["holding-id-1-item-1", "holding-id-1-item-2"],
                ["holding-id-2-item-1", "holding-id-2-item-2"],
            ]
            self.assertEqual(id_list, expected_result)
            # Verify that the mock functions were called with the correct arguments
            mock_auth.assert_called_once_with(
                self.url, self.username, self.password, self.tenant
            )
            mock_get_instances.assert_called_once_with(
                mock_token, self.url, self.hrid, self.tenant
            )
            # Verify that the mock get_holdings function was called twice with different instance IDs
            calls = [
                unittest.mock.call(mock_token, self.url, "instance-id-1", self.tenant),
                unittest.mock.call(mock_token, self.url, "instance-id-2", self.tenant),
            ]
            mock_get_holdings.assert_has_calls(calls)
            # Verify that the mock get_items function was called twice with different holding IDs
            calls = [
                unittest.mock.call(mock_token, self.url, "holding-id-1", self.tenant),
                unittest.mock.call(mock_token, self.url, "holding-id-2", self.tenant),
            ]
            mock_get_items.assert_has_calls(calls)

            # Verify that the print function was called four times with empty strings
            calls = [
                unittest.mock.call(''),
                unittest.mock.call(''),
                unittest.mock.call(''),
                unittest.mock.call(''),
            ]
            mock_print.assert_has_calls(calls)

    @patch('folio_curl.get_items')
    @patch('folio_curl.get_holdings')
    @patch('folio_curl.get_instances')
    @patch('folio_curl.auth')
    def test_invalid_hrid(
        self, mock_auth, mock_get_instances, mock_get_holdings, mock_get_items
    ):
        mock_token = "valid-token"
        mock_item_ids_1 = ["item-id-1", "item-id-2"]
        mock_item_ids_2 = ["item-id-3", "item-id-4"]
        mock_auth.return_value = mock_token
        mock_get_instances.return_value = None  # invalid hrid returns None
        mock_get_holdings.return_value = ["holding-id-1", "holding-id-2"]
        mock_get_items.side_effect = [mock_item_ids_1, mock_item_ids_2]
        with patch('builtins.print') as mock_print:
            id_list = get_records(
                self.url, self.username, self.password, self.tenant, "invalid-hrid"
            )
            # id_list should be an empty list for invalid hrid
            self.assertEqual(id_list, [])
            mock_auth.assert_called_once_with(
                self.url, self.username, self.password, self.tenant
            )
            mock_get_instances.assert_called_once_with(
                mock_token, self.url, "invalid-hrid", self.tenant
            )
            # the following mocks should not be called for invalid hrid
            mock_get_holdings.assert_not_called()
            mock_get_items.assert_not_called()
            # verify that print statements are correctly suppressed
            expected_calls = [unittest.mock.call(''), unittest.mock.call('')]
            mock_print.assert_has_calls(expected_calls)


if __name__ == "__main__":
    unittest.main()
