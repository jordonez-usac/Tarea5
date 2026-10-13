import json
import socket
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

items = []


class Handler(BaseHTTPRequestHandler):
    def send(self, code, data):
        body = json.dumps(data).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path == "/":
            self.send(200, {"mensaje": "API MIA Tarea 5", "host": socket.gethostname()})
        elif self.path == "/health":
            self.send(200, {"status": "ok"})
        elif self.path == "/items":
            self.send(200, items)
        else:
            self.send(404, {"error": "no encontrado"})

    def do_POST(self):
        if self.path != "/items":
            return self.send(404, {"error": "no encontrado"})
        try:
            data = json.loads(self.rfile.read(int(self.headers.get("Content-Length", 0))))
        except ValueError:
            return self.send(400, {"error": "json invalido"})
        item = {"id": len(items) + 1, "data": data}
        items.append(item)
        self.send(201, item)


if __name__ == "__main__":
    print("Escuchando en 0.0.0.0:8000")
    ThreadingHTTPServer(("0.0.0.0", 8000), Handler).serve_forever()
