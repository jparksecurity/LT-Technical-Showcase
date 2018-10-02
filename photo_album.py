import requests
import datetime

# Global values
base = "https://jsonplaceholder.typicode.com/photos{}"
F = open("error.txt","w")

def Check_Acceptance():
    try:
        id = eval(input("Enter which album you want to see(1 - 100):"))
        if type(id) == int and id > 0 and id <= 100:
            return id
        else:
            raise NameError()
    except NameError:
        F.write("{} - Invalid input. Please type integer from 1 to 100.\n".format(datetime.datetime.now()))
        raise NameError("Invalid input. Please type integer from 1 to 100.")

def Fetch_Album(n):
    url = base.format("?albumId={}".format(n))
    resp = requests.get(url)
    resp.close()
    if resp.status_code != 200 or resp.json() == []:
        F.write("{} - Failed to retrieve data.\n".format(datetime.datetime.now()))
        raise Exception("Failed to retrieve data")
    return resp.json()

def Parse_Album(jsons):
    IDandTitle = []
    for json in jsons:
        IDandTitle.append([json['id'], json['title']])
        print("[{}]".format(json['id']), json['title'])
    return IDandTitle

if __name__ == "__main__":
    id = Check_Acceptance()
    data = Fetch_Album(id)
    Parse_Album(data)
    F.close()
