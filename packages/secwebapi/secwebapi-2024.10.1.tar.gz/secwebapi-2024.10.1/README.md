# Secwe AI-Powered Detection of Malicious Domains

## Secweb API Overview

`secwebapi` is a Python package designed to interact with the Secwe API. It provides a simple and intuitive interface for sending requests and processing responses from the API.

## Installation

To install `secwebapi`, you need to have Python installed on your system. If you don't have Python installed, you can download it from the official website.

Once Python is installed, you can install `secwebapi` by cloning the repository and running the setup script:
```bash
python3 -m pip install secwebapi
```
or by running the following commands in your terminal:
```bash
git clone https://github.com/sametazaboglu/secwebapi.git
cd secwebapi
pip install .
```

## Example Usage

Here's an example of how you can use `secwebapi` to send a request to the Secweb API:

```python
import secwebapi

# Initialize the API with your credentials
USERNAME = ''
API_KEY = ''

web_client = secwebapi.Secweb(
    USERNAME,
    API_KEY
)


# Read domains from a file and store the results
web_client.read_domains_from_file('domains.txt')

# Access the results property
for domain, prediction in web_client.results:
    print(f"Domain: {domain}")
    print(f"Prediction: {prediction}\n")
```

# STAY SAFE
