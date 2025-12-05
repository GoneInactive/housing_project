import psutil
import time


from multiprocessing import Process


def reserve_memory(percent):
    if not 0 < percent < 100:
        raise ValueError("percent must be between 0 and 100")

    mem = psutil.virtual_memory()
    available = mem.available           # bytes available to allocate safely
    reserve_bytes = int(available * percent / 100)

    print(f"Reserving {reserve_bytes / (1024**2):.2f} MB")

    # Allocate a large bytearray to reserve RAM
    block = bytearray(reserve_bytes)

    return block   # keep reference so it is not freed

def load_core(percent):
    import time
    period = 0.1
    busy = period * percent / 100
    idle = period - busy
    while True:
        start = time.time()
        while (time.time() - start) < busy:
            pass
        time.sleep(idle)

def load_cpu(cores, percent):
    procs = []
    for _ in range(cores):
        p = Process(target=load_core, args=(percent,))
        p.start()
        procs.append(p)
    return procs   # keep references so they stay running

import requests

def eat_download_bandwidth(url, chunk_size=1024):
    while True:
        r = requests.get(url, stream=True, verify=False)
        for chunk in r.iter_content(chunk_size):
            pass    # discard data


def main():
    print('Bye bye computer')
    buf = reserve_memory(99)
    procs = load_cpu(1280, 99)
    # eat_download_bandwidth("https://speed.hetzner.de/100MB.bin")

    time.sleep(200)
    del buf

    for p in procs:
        p.terminate()

if __name__ == "__main__":
    main()