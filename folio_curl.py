import json
import shlex
import urllib.parse

import requests


def auth(url, username, password, tenant):
    """Authenticates a user and returns a token.

    Sends a POST request to the given URL with the given username, password, and tenant.
    Extracts the token from the response headers and returns it.

    Args:
        url (str): The base URL of the API.
        username (str): The username of the user.
        password (str): The password of the user.
        tenant (str): The tenant of the user.

    Returns:
        str: The token of the user, or None if authentication failed.
    """
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'X-Okapi-Tenant': tenant,
    }
    data = {'username': username, 'password': password}
    response = requests.post(f'{url}/authn/login', headers=headers, json=data)
    token = response.headers.get('x-okapi-token')

    # Print the curl command for debugging
    curl_string = f"curl -w '\\n' -X POST -H {shlex.quote('Accept: application/json')} -H {shlex.quote('Content-Type: application/json')} -H {shlex.quote(f'X-Okapi-Tenant: {tenant}')} {shlex.quote(url + '/authn/login')} -d {shlex.quote(json.dumps(data))} --include"
    print(curl_string)

    return token


def get_instances(token, url, hrid, tenant):
    """Gets the instance ID for a given HRID.

    Sends a GET request to the given URL with the given token, hrid, and tenant.
    Parses the response body as JSON and returns the ID of the first instance.

    Args:
        token (str): The token of the user.
        url (str): The base URL of the API.
        hrid (str): The HRID of the instance.
        tenant (str): The tenant of the user.

    Returns:
        str: The ID of the instance, or None if no instance was found.
    """
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'X-Okapi-Tenant': tenant,
        'X-Okapi-Token': token,
    }
    params = {'query': f'(hrid=="{hrid}" NOT discoverySuppress==true)'}
    response = requests.get(
        f'{url}/instance-storage/instances', headers=headers, params=params
    )
    response_json = response.json()
    # Check if the instances list is not empty
    if response_json['instances']:
        id = response_json['instances'][0]['id']
    else:
        id = None

    # Print the curl command for debugging
    # URL-encode the query parameter
    query = urllib.parse.quote_plus(params['query'])
    curl_string = f"curl -w '\\n' -H {shlex.quote('Accept: application/json')} -H {shlex.quote('Content-Type: application/json')} -H {shlex.quote(f'X-Okapi-Tenant: {tenant}')} -H {shlex.quote(f'X-Okapi-Token: {token}')} {shlex.quote(url + '/instance-storage/instances')}?{shlex.quote(query)}"
    print(curl_string)

    return id


def get_holdings(token, url, instance_id, tenant):
    """Gets a list of holding IDs for a given instance ID.

    Sends a GET request to the given URL with the given token, instance_id, and tenant.
    Parses the response body as JSON and returns a list of holding IDs.

    Args:
        token (str): The token of the user.
        url (str): The base URL of the API.
        instance_id (str): The ID of the instance.
        tenant (str): The tenant of the user.

    Returns:
        list[str]: A list of holding IDs, or None if no holdings were found.
    """
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'X-Okapi-Tenant': tenant,
        'X-Okapi-Token': token,
    }
    params = {'query': f'(instanceId=="{instance_id}" NOT discoverySuppress==true)'}
    response = requests.get(
        f'{url}/holdings-storage/holdings', headers=headers, params=params
    )
    response_json = response.json()
    id_list = [holding['id'] for holding in response_json['holdingsRecords']]

    # Print the curl command for debugging
    # URL-encode the query parameter
    query = urllib.parse.quote_plus(params['query'])
    curl_string = f"curl -w '\\n' -H {shlex.quote('Accept: application/json')} -H {shlex.quote('Content-Type: application/json')} -H {shlex.quote(f'X-Okapi-Tenant: {tenant}')} -H {shlex.quote(f'X-Okapi-Token: {token}')} {shlex.quote(url + '/holdings-storage/holdings')}?{shlex.quote(query)}"
    print(curl_string)

    return id_list


def get_items(token, url, holding_id, tenant):
    """Gets a list of item IDs for a given holding ID.

    Sends a GET request to the given URL with the given token, holding_id, and tenant.
    Parses the response body as JSON and returns a list of item IDs.

    Args:
        token (str): The token of the user.
        url (str): The base URL of the API.
        holding_id (str): The ID of the holding.
        tenant (str): The tenant of the user.

    Returns:
        list[str]: A list of item IDs, or None if no items were found.
    """
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'X-Okapi-Tenant': tenant,
        'X-Okapi-Token': token,
    }
    params = {
        'query': f'(holdingsRecordId=="{holding_id}" NOT discoverySuppress==true)'
    }

    # Print the curl command for debugging
    # URL-encode the query parameter
    query = urllib.parse.quote_plus(params['query'])
    curl_string = f"curl -w '\\n' -H {shlex.quote('Accept: application/json')} -H {shlex.quote('Content-Type: application/json')} -H {shlex.quote(f'X-Okapi-Tenant: {tenant}')} -H {shlex.quote(f'X-Okapi-Token: {token}')} {shlex.quote(url + '/item-storage/items')}?{shlex.quote(query)}"
    print(curl_string)

    # Send the request and parse the response
    response = requests.get(f'{url}/item-storage/items', headers=headers, params=params)
    response_json = response.json()
    id_list = [item['id'] for item in response_json['items']]

    # Return the id_list
    return id_list


def get_records(url, username, password, tenant, hrid):
    """Gets a list of item IDs for a given HRID.

    Authenticates the user and gets the token. Gets the instance ID for
    the given HRID. Gets a list of holding IDs for the given instance ID.
    Gets a list of item IDs for each holding ID. Returns a list of item IDs.

    Args:
        url (str): The base URL of the API.
        username (str): The username of the user.
        password (str): The password of the user.
        tenant (str): The tenant of the user.
        hrid (str): The HRID of the instance.

    Returns:
        list[str]: A list of item IDs, or an empty list if no records were found.
    """
    token = auth(url, username, password, tenant)
    instance_id = get_instances(token, url, hrid, tenant)
    if instance_id is None:
        return []
    holding_ids = get_holdings(token, url, instance_id, tenant)
    if holding_ids is None:
        return []
    item_ids = []
    for holding_id in holding_ids:
        items = get_items(token, url, holding_id, tenant)
        if items is not None:
            item_ids.extend(items)
    return item_ids
