"""
Pre-defined GET functions
"""

import json

import requests
from constants import AUTH_HEADER
import os
import math
import concurrent.futures


def get_sets() -> dict | None:
    response = requests.get("https://api.pokeapi.co/v2/sets", headers=AUTH_HEADER)

    if response.status_code == 200:
        return response.json()

    print(response.text)
    return None


def get_set(set_id: str) -> list[dict]:
    # First check if the file exists
    if os.path.exists(f"set_data/{set_id}.json"):
        print(f"get_set({set_id}): loading from set_data/{set_id}.json")
        with open(f"set_data/{set_id}.json", "r") as file:
            return json.load(file)

    # Get No. of Pages
    url = f"https://api.pokemontcg.io/v2/cards?q=set.id:{set_id}&page=1&select=id"
    print(f"get_set({set_id}): Making request to {url}")
    response = requests.get(url, headers=AUTH_HEADER)
    data = response.json()

    ps = data.get("pageSize", 1.0)
    cnt = data.get("totalCount", 0.0)
    num_pages = math.ceil(cnt / ps)

    print(f"get_set({set_id}): Set has {num_pages} pages.")
    params = [(set_id, i) for i in range(1, num_pages + 1)]

    num_workers = max(num_pages, 5)
    print(f"get_set({set_id}): Starting Thread Pool with {num_workers} workers.")
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_workers) as executor:
        results_iterator = executor.map(lambda p: get_page(p[0], p[1]), params)
        all_results = list(results_iterator)

    with open(f"set_data/{set_id}.json", "w") as file:
        print(f"get_set({set_id}): saving to set_data/{set_id}.json")
        json.dump(all_results, file, indent=4)

    return all_results


def get_page(set_id: str, page: int) -> dict:
    url = (
        f"https://api.pokemontcg.io/v2/cards?q=set.id:{set_id}&page={page}&pageSize=250"
    )
    print(f"get_page({set_id}, {page}): Page {page}: Requesting {url}")
    return requests.get(url, headers=AUTH_HEADER).json()
