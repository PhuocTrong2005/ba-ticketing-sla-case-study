"""Use the existing Git credential in memory; never print or persist it.

Small GitHub REST helper for authorized Pages setup and deployment inspection.
"""
import argparse
import json
import subprocess
import urllib.request
import urllib.error

REPO = 'PhuocTrong2005/ba-ticketing-sla-case-study'


def api(path, method='GET', body=None):
    result = subprocess.run(['git', 'credential', 'fill'],
                            input='protocol=https\nhost=github.com\n\n',
                            capture_output=True, text=True, check=True)
    credential = dict(line.split('=', 1) for line in result.stdout.splitlines() if '=' in line)
    token = credential.get('password')
    if not token:
        raise RuntimeError('No existing GitHub credential available')
    req = urllib.request.Request('https://api.github.com/repos/' + REPO + path,
        data=json.dumps(body).encode() if body is not None else None,
        method=method, headers={'Authorization': 'Bearer ' + token,
        'Accept': 'application/vnd.github+json', 'X-GitHub-Api-Version': '2022-11-28',
        'User-Agent': 'ticketing-pages-check', 'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            raw = response.read()
            return json.loads(raw) if raw else {'status': response.status}
    except urllib.error.HTTPError as error:
        return {'http_error': error.code, 'details': json.loads(error.read())}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('path', nargs='?', default='')
    parser.add_argument('--method', default='GET', choices=['GET', 'POST', 'PUT'])
    parser.add_argument('--body')
    args = parser.parse_args()
    print(json.dumps(api(args.path, args.method, json.loads(args.body) if args.body else None), indent=2))
