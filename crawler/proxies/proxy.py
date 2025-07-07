import os
import random
from crawler.proxies.proxies_checker import make_working_list

from paths.paths import working_proxies_path

def get_working_proxy(test_url):

    while not os.path.exists(working_proxies_path) or os.path.getsize(working_proxies_path) == 0:
        make_working_list(test_url)
    

    with open(working_proxies_path, "r") as f:
        working_proxies = f.read().split("\n")
    
    proxy = random.choice(working_proxies)
    print("got a proxy!")
    return proxy
    

