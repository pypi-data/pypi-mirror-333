import aiohttp
import asyncio
import tldextract
import ssl


class Secweb:
    def __init__(self, username='', api_key=''):
        self.api_key = api_key
        self.base_url = f"https://secwe.pythonanywhere.com/api/predict/"
        self.headers = {
            "X-User": username,
            "Authorization": f"{self.api_key}",
        }

        self.domain = None
        self.prediction = None

        self.response = None

    async def __async_get(self, domain):
        sslcontext = ssl.create_default_context()
        sslcontext.check_hostname = False
        sslcontext.verify_mode = ssl.CERT_NONE

        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.base_url}{domain}", headers=self.headers, ssl=sslcontext) as response:
                if response.status == 200:
                    return self.__parse_response(await response.json())
                elif response.status == 403:
                    return None, f"\nInvalid username, password or API key: {response.status}"
                elif response.status == 429:
                    return None, f"\nRate limit exceeded: {response.status}"
                else:
                    return None, f"\nRequest failed with status code {response.status}"

    def __parse_response(self, response):
        if isinstance(response, dict):
            try:
                self.domain = response['domain']
                self.prediction = response['prediction']
                return self.domain, self.prediction
            except KeyError:
                return "Invalid response format"
        else:
            return "Response is not a dictionary"

    async def __async_read_domains_from_file(self, file_path, verbose=True):
        self.results = []
        with open(file_path, 'r') as file:
            for line in file:
                domain, *category = line.strip().split()
                category = ' '.join(category)
                extracted = tldextract.extract(domain)
                if not extracted.subdomain and extracted.suffix:
                    self.domain, self.prediction = await self.__async_get(domain)
                    if verbose:
                        print(f"Domain: {self.domain}, Prediction: {self.prediction}")
                    self.results.append((self.domain, self.prediction))
                else:
                    print(f"'{domain}' is not a valid domain.")

    def read_domains_from_file(self, file_path, verbose=True):
        asyncio.run(self.__async_read_domains_from_file(file_path, verbose))

    def get(self, domain):
        return asyncio.run(self.__async_get(domain))
    