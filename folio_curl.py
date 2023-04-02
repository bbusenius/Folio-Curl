import argparse
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
    """Gets the instance ID(s) for a given HRID.
    Sends a GET request to the given URL with the given token, hrid, and tenant.
    Parses the response body as JSON and returns the ID(s) of the instances.

    Args:
        token (str): The token of the user.
        url (str): The base URL of the API.
        hrid (str): The HRID of the instance.
        tenant (str): The tenant of the user.

    Returns:
        list[str]: The IDs of the instances, or an empty list if no instances were found.
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
    try:
        response_json = response.json()
    except json.decoder.JSONDecodeError:
        print(
            "Error: Failed to parse response as JSON. You probably don't have access to okapi."
        )
        return []

    # Check if the instances list is not empty
    if response_json['instances']:
        ids = [instance['id'] for instance in response_json['instances']]
    else:
        ids = []

    # Print the curl command for debugging
    # URL-encode the query parameter
    query = urllib.parse.quote_plus(params['query'])
    curl_string = f"curl -w '\\n' -H {shlex.quote('Accept: application/json')} -H {shlex.quote('Content-Type: application/json')} -H {shlex.quote(f'X-Okapi-Tenant: {tenant}')} -H {shlex.quote(f'X-Okapi-Token: {token}')} {shlex.quote(url + '/instance-storage/instances')}?{shlex.quote(query)}"
    print(curl_string)

    return ids


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
    try:
        response = requests.get(
            f'{url}/holdings-storage/holdings', headers=headers, params=params
        )
        response_json = response.json()
    except json.JSONDecodeError:
        print(
            "Error: Failed to parse response as JSON. You probably don't have access to okapi."
        )
        return None

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
        list[str]: A list of item IDs, or an empty list if no items were found.
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
    try:
        response = requests.get(
            f'{url}/item-storage/items', headers=headers, params=params
        )
        response_json = response.json()
        id_list = [item['id'] for item in response_json['items']]
    except json.JSONDecodeError:
        print("Error: Response body could not be parsed as JSON")
        id_list = []

    # Return the id_list
    return id_list


def get_records(url, username, password, tenant, hrid):
    """Gets a list of lists of item IDs for a given HRID.
    Authenticates the user and gets the token. Gets the instance IDs for
    the given HRID. Gets a list of holding IDs for each instance ID.
    Gets a list of item IDs for each holding ID. Returns a list of lists of item IDs,
    where each list corresponds to a different holding ID.

    Args:
        url (str): The base URL of the API.
        username (str): The username of the user.
        password (str): The password of the user.
        tenant (str): The tenant of the user.
        hrid (str): The HRID of the instance.

    Returns:
        list[list[str]]: A list of lists of item IDs, or an empty list if no records were found.
    """
    token = auth(url, username, password, tenant)
    print('')  # Added print statement after auth
    instance_ids = get_instances(token, url, hrid, tenant)
    print('')  # Added print statement after get_instances
    if not instance_ids:
        return []
    item_ids = []
    for instance_id in instance_ids:
        holding_ids = get_holdings(token, url, instance_id, tenant)
        print('')  # Added print statement after get_holdings
        if holding_ids:
            for holding_id in holding_ids:
                items = get_items(token, url, holding_id, tenant)
                print('')  # Added print statement after get_items
                if items is not None:
                    # Changed from extend to append to create a list of lists
                    item_ids.append(items)
    return item_ids


def main():
    """Main entry point for the script."""
    # Create an argument parser
    parser = argparse.ArgumentParser(description='Get records from FOLIO using curl.')
    # Add arguments for FOLIO URL, username, password, tenant ID and hrid
    parser.add_argument('url', help='FOLIO URL')
    parser.add_argument('username', help='FOLIO username')
    parser.add_argument('password', help='FOLIO password')
    parser.add_argument('tenant', help='FOLIO tenant ID')
    parser.add_argument('hrid', help='Human-readable ID of the record to fetch')
    # Parse the arguments
    args = parser.parse_args()
    # Call the get_records function with the arguments
    get_records(args.url, args.username, args.password, args.tenant, args.hrid)
