from flask import Flask, request, Response
import requests
import os

app = Flask(__name__)

@app.route('/', defaults={'path': ''}, methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS'])
@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS'])
def proxy(path):
    scheme = request.args.get("scheme", "http")
    hidden_service = os.getenv("HIDDEN_SERVICE")
    if not hidden_service:
        return "No .onion target defined.", 500

    url = f"{scheme}://{hidden_service}/{path}"
    try:
        resp = requests.request(
            method=request.method,
            url=url,
            headers={key: value for key, value in request.headers},
            data=request.get_data(),
            cookies=request.cookies,
            proxies={
                'http': 'socks5h://tor-socks5:9050',
                'https': 'socks5h://tor-socks5:9050'
            },
            timeout=30,
            verify=False
        )

        excluded_headers = ['content-encoding', 'transfer-encoding', 'content-length']
        headers = [(name, value) for (name, value) in resp.headers.items() if name.lower() not in excluded_headers]

        return Response(
            resp.content,
            status=resp.status_code,
            headers=headers,
            content_type=resp.headers.get('Content-Type', 'text/html')
    )
    except Exception as e:
        return f"Failed to reach hidden service: {e}", 502

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
