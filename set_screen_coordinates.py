import sys
from pymemcache.client.base import Client


if __name__ == '__main__':
    client = Client('localhost')
    client.set('front_window_frame', sys.argv[1])