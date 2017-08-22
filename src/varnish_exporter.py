from prometheus_client import start_http_server
from prometheus_client.core import REGISTRY

import json, requests, sys, time, os, ast, signal


from varnish_class import VarnishCollector


def sigterm_handler(_signo, _stack_frame):
  sys.exit(0)

if __name__ == '__main__':
  # Ensure we have something to export
  if not (os.getenv('BIND_PORT') or os.getenv('VARNISH_NAME') or os.getenv('VARNISH_HOST') or os.getenv('VARNISH_PORT') ):
    print("No BIND_PORT or VARNISH_NAME or VARNISH_HOST or VARNISH_PORT specified, exiting")
    exit(1)


  start_http_server(int(os.getenv('BIND_PORT')))
  REGISTRY.register(VarnishCollector(
      os.getenv('VARNISH_NAME'),
      os.getenv('VARNISH_HOST'),
      int(os.getenv('VARNISH_PORT')),
      os.getenv('VARNISH_USER'),
      os.getenv('VARNISH_PASSWORD')
    )
  )

  signal.signal(signal.SIGTERM, sigterm_handler)
  while True: time.sleep(1)
