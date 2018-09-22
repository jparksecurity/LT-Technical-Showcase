import requests
try: input = raw_input
except NameError: pass

# Global values
base = "https://jsonplaceholder.typicode.com/photos{}"
id = input("Enter which album you want to see:")

# Fetch the photo album n from the database
def fetch(n):
    url = base.format("?albumId={}".format(n))
    resp = requests.get(url)
    resp.close()
    if resp.status_code != 200:
        raise Exception(resp,json()['detail'])
    return resp.json()

# Parse the json to print
def parse(jsons):
    for json in jsons:
        print("[{}]".format(json['id']), json['title'])

data = fetch(id)
parse(data)
