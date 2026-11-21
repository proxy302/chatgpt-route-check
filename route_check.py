#!/usr/bin/env python3
"""Does OpenAI accept the network location of this connection or proxy?
Sends one unauthenticated request to the OpenAI API and reads the answer:
  401 (no API key)                               -> location accepted at network level
  403 unsupported_country_region_territory       -> location not supported
It also prints the exit IP's country and network from ipinfo.io.

usage: python3 route_check.py                                   (your own connection)
       python3 route_check.py --proxy http://USER:PASS@HOST:PORT
No API key is sent and no account is used. Standard library only.
"""
import json, sys, urllib.error, urllib.request

def opener(proxy):
    return urllib.request.build_opener(*([urllib.request.ProxyHandler({'http': proxy, 'https': proxy})] if proxy else []))

def get(op, url):
    try:
        with op.open(urllib.request.Request(url, headers={'User-Agent': 'route-check/1.0'}), timeout=20) as r:
            return r.status, r.read()
    except urllib.error.HTTPError as e:
        return e.code, e.read()

def main():
    proxy = sys.argv[2] if len(sys.argv) > 2 and sys.argv[1] == '--proxy' else None
    op = opener(proxy)
    _, body = get(op, 'https://ipinfo.io/json')
    info = json.loads(body)
    print(f"Exit IP     {info.get('ip')}  {info.get('country')} {info.get('city', '')}")
    print(f"Network     {info.get('org', '?')}")
    status, body = get(op, 'https://api.openai.com/v1/models')
    try:
        err = json.loads(body).get('error') or {}
    except ValueError:
        err = {}
    code = err.get('code') or err.get('type') or ''
    print(f"OpenAI API  HTTP {status} {code}")
    if status == 401:
        print('Verdict     accepted: the API answered "no key", so this location passes the network check')
    elif status == 403 and 'unsupported_country' in str(code):
        print('Verdict     not supported: OpenAI does not serve this location')
    else:
        print('Verdict     unclear: see the status and error code above')
    print('Note        this tests the route only. Where you are, not the IP, decides whether you may use ChatGPT;')
    print('            see https://help.openai.com/en/articles/7947663-chatgpt-supported-countries')

if __name__ == '__main__':
    main()
