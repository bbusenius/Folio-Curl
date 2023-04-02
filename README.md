## folio_curl
`folio_curl` is a Python utility that makes requests to the FOLIO okapi API and prints corresponding curl commands for debugging purposes. This script can be installed from GitHub via pip and requires the user to pass in several arguments. The utility contains three main functions: `auth()`, `get_instances()`, and `get_holdings()`.

### Installation
To install `folio_curl`, use the following `pip` command:

```sh
pip install git+https://github.com/bbusenius/folio_curl.git
```

### Usage
`folio_curl` requires five arguments to be passed in when used:

```
folio_curl url username password tenant hrid
```
where:

- **url**: The base URL of the FOLIO API.
- **username**: The username of the user.
- **password**: The password of the user.
- **tenant**: The tenant of the user.
- **hrid**: The HRID of the instance.

Once installed and called, `folio_curl` will authenticate the user, retrieve the instance ID for the given HRID, and then retrieve a list of holding IDs for the instance. In each of these functions, a curl command is printed for debugging purposes.

#### Example Usage

```
folio_curl https://my-folio-instance.com my-username my-password my-tenant my-instance-hrid
```

#### Python Usage

```
import folio_curl

url = "https://my-folio-instance.com"
username = "my-username"
password = "my-password"
tenant = "my-tenant"
hrid = "my-instance-hrid"

token = folio_curl.auth(url, username, password, tenant)
instance_ids = folio_curl.get_instances(token, url, hrid, tenant)
instance_id = instance_ids[0]  # Assuming there is only one instance with the given HRID
holdings = folio_curl.get_holdings(token, url, instance_id, tenant)

print(holdings)
```

### Testing
`folio_curl` contains unit tests in `tests/test_folio_curl.py`. These tests can be run with the following command:

```
python3 -m unittest discover tests -p 'test_*.py'
```

