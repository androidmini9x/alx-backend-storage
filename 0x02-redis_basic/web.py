#!/usr/bin/env python3
"""Task 5 Module"""
import redis
import requests
rc = redis.Redis()
count = 0


def get_page(url: str) -> str:
    """obtain the HTML content of a particular URL and returns it"""
    rc.set(f"cached:{url}", count)
    resp = requests.get(url)
    rc.incr(f"count:{url}")
    rc.setex(f"cached:{url}", 10, rc.get(f"cached:{url}"))
    return resp.text


if __name__ == "__main__":
    """Main Function"""
    get_page('http://slowwly.robertomurray.co.uk')