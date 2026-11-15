#!/usr/bin/env python3
"""Buyer dashboard for one traffic source: the Chatterfy funnel of the campaigns whose name contains CAMPAIGN_MATCH.
No database and no Chatterfy keys here: everything comes from the shared sync service (dmavens-stat-cf) at CF_URL.

Env: CF_URL, CAMPAIGN_MATCH (FB / Google), TITLE        Run: python3 server.py [port]
"""
import json, os, sys, urllib.parse, urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

ROOT = os.path.dirname(os.path.abspath(__file__))
CF_URL = os.environ.get('CF_URL', 'http://localhost:8079').rstrip('/')
MATCH = os.environ.get('CAMPAIGN_MATCH', 'FB')
TITLE = os.environ.get('TITLE', MATCH)
API = {'/api/funnel', '/api/leads', '/api/sync', '/api/status'}  # -> CF_URL/funnel ... with the campaign filter fixed server-side


class H(BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def do_GET(self):
        u = urllib.parse.urlparse(self.path)
        code, ctype = 200, 'application/json'
        try:
            if u.path == '/':
                body, ctype = open(os.path.join(ROOT, 'index.html'), 'rb').read().replace(b'{{TITLE}}', TITLE.encode()), 'text/html'
            elif u.path == '/style.css':
                body, ctype = open(os.path.join(ROOT, 'style.css'), 'rb').read(), 'text/css'
            elif u.path in API:
                q = urllib.parse.parse_qs(u.query)
                params = {'match': MATCH, **{k: q[k][0] for k in ('date_from', 'date_to') if k in q}}
                with urllib.request.urlopen(f'{CF_URL}{u.path[4:]}?{urllib.parse.urlencode(params)}', timeout=120) as r:
                    body = r.read()
            else:
                code, body = 404, b'{"error": "not found"}'
        except Exception as e:  # sync service down / restarting
            code, body = 502, json.dumps({'error': f'сервис Chatterfy недоступен: {e}'}, ensure_ascii=False).encode()
        self.send_response(code)
        self.send_header('Content-Type', ctype + '; charset=utf-8')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)


if __name__ == '__main__':
    port = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].isdigit() else 8080
    print(f'{TITLE} dashboard: http://localhost:{port}/  (campaigns ~ "{MATCH}", data from {CF_URL})', flush=True)
    ThreadingHTTPServer(('0.0.0.0', port), H).serve_forever()
