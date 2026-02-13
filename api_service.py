import requests
def fetchAPIData(barcode):
    url = f"https://world.openfoodfacts.org/api/v0/product/{barcode}.json"
    response = requests.get(url)
    return response.json()

fetchAPIData(5000159376792)