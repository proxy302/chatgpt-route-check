# chatgpt-route-check: does OpenAI accept this network location?

Send one unauthenticated request to the OpenAI API through your connection or a proxy and read the reply: `401` means the request reached OpenAI and was refused only for the missing key, so the location passes the network-level check; `403` with the error code `unsupported_country_region_territory` means OpenAI does not serve that location. `route_check.py` does this with the Python standard library, prints the exit IP's country and network next to it, and never sends a key or touches an account. It tests the route, not your eligibility: OpenAI offers ChatGPT only in the countries on its [supported countries list](https://help.openai.com/en/articles/7947663-chatgpt-supported-countries), and that list is about where you are, not where an IP points. Proxy302 maintains this tool and sells static ISP IPs, including a GPT/Grok tier meant for keeping one ChatGPT account on one IP.

> Maintained by [Proxy302](https://proxy302.com). MIT licensed.

## Usage

```bash
python3 route_check.py
python3 route_check.py --proxy "http://USER:PASS@HOST:PORT"
```

USER, PASS, HOST and PORT are placeholders; percent-encode `@ # : /` in the password. Python 3.8+, no packages to install.

Output on an accepted route (exit IP lines omitted):

```text
OpenAI API  HTTP 401 invalid_request_error
Verdict     accepted: the API answered "no key", so this location passes the network check
```

The same test with curl:

```bash
curl -sS -o /dev/null -w "%{http_code}\n" -x "http://USER:PASS@HOST:PORT" https://api.openai.com/v1/models
```

## Reading the result

| Reply | Meaning |
|---|---|
| `401`, no key | The location passes OpenAI's network check |
| `403` `unsupported_country_region_territory` | OpenAI does not serve this location |
| Timeout or TLS error | A problem with the connection or proxy, not with OpenAI's location rules |
| Anything else | Read the status and error code; the script does not guess |

## What this does not tell you

- **Whether you may use ChatGPT.** That depends on where you are. OpenAI warns that using its services from outside the listed countries may get an account blocked or suspended, and an IP does not change where you are.
- **Anything about your account.** Payment problems, verification requests and policy enforcement have nothing to do with this test.
- **Whether the IP looks residential.** For that, check the network type in IP databases; see [what a dual ISP IP is](https://github.com/proxy302/proxy-guides/blob/main/what-is-dual-isp-ip/README.md) and [ip-native-check](https://github.com/proxy302/ip-native-check).

## Related

- [Which IP for a long-term ChatGPT Plus or Pro account?](https://github.com/proxy302/chatgpt-account-dedicated-ip)
- [What IP should I use for Claude and ChatGPT?](https://github.com/proxy302/proxy-guides/blob/main/which-ip-for-claude-and-chatgpt/README.md)

*Checked 21 November 2026.*
