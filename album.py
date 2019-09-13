"""List IDs and titles of a user chosen album.

Usage:

    python3 album.py
"""

import logging

import requests

from settings import (PROMPT, INPUT_WARNING_MESSAGE, INPUT_WARNING_MESSAGE_USER,
                     SERVER_ERROR_MESSAGE, URL)

logging.basicConfig(filename='album.log',
    format='%(asctime)s %(levelname)-8s %(message)s',
    datefmt='%a, %d %b %Y %H:%M:%S',
    level=logging.INFO)

def validate_input():
    """Validate user input to accept only legitimate ID.

    Returns:
        Valid integer user input from 1 to 100. Otherwise, -1.
    """
    try:
        album_id = int(input(PROMPT))
        if type(album_id) is not int or not 1 <= album_id <= 100:
            raise ValueError
    except ValueError:
        logging.warning(INPUT_WARNING_MESSAGE)
        print(INPUT_WARNING_MESSAGE_USER)
        return -1
    else:
        return album_id


def fetch_album(album_id):
    """Fetch album from server to get data containing ID and title.

    Args:
        album_id: User given album id.
    Raises:
        RuntimeError: If the server doesn't response properly
    Returns:
        Data set of a certain album in JSON.
    """
    response = requests.get(URL.format(album_id), timeout=5)
    response.close()
    if response.status_code != 200 or not response.json():
        logging.error(SERVER_ERROR_MESSAGE)
        raise RuntimeError(SERVER_ERROR_MESSAGE)
    return response.json()


def parse_album(data):
    """Parse JSON to list desired IDs and titles.

    Args:
        data: A list of JSON containg 'id' and 'title'
    """
    for json in data:
        print(f"[{json['id']}] {json['title']}")


def main():
    album_id = -1
    while album_id == -1:
        album_id = validate_input()
    data = fetch_album(album_id)
    parse_album(data)


if __name__ == "__main__":
    main()
