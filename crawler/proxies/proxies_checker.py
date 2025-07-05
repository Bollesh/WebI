import requests
import threading
from queue import Queue

from paths.paths import all_proxies_path, working_proxies_path

all_proxies = []
working_proxies = []
q = Queue()

with open(all_proxies_path, "r", encoding="utf-8") as f:
    all_proxies = f.read().split("\n")

for proxy in all_proxies:
    q.put(proxy)

def proxy_check(test_url):
    global q
    while not q.empty():
        proxy = q.get()
        try:
            test_res = requests.get(
                url=test_url,
                proxies={
                    "http": proxy,
                    "https": proxy
                },
                timeout=15
            )
        except:
            continue
        
        if test_res.status_code == 200:
            working_proxies.append(proxy)
            print(proxy)




def make_working_list(test_url):
    print("Generating a list of working proxies\n")
    threads = []
    for _ in range(100):
        thread = threading.Thread(target=proxy_check, kwargs={'test_url': test_url})
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    print("Checked all proxies...\n")
    with open(working_proxies_path, "w", encoding="utf-8") as f:
        f.write("\n".join(working_proxies))



