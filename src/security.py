from tornado.web import RequestHandler

# Cubre: CSP (CWE-693), Clickjacking (CWE-1021), MIME-sniffing (CWE-693)
_HEADERS = {
    "Content-Security-Policy": (
        "default-src 'self'; "
        "script-src 'self' 'unsafe-inline' 'unsafe-eval'; "
        "style-src 'self' 'unsafe-inline'; "
        "img-src 'self' data: blob:; "
        "font-src 'self' data:; "
        "connect-src 'self' ws: wss:; "
        "frame-ancestors 'none';"
    ),
    "X-Frame-Options": "DENY",
    "X-Content-Type-Options": "nosniff",
    "Referrer-Policy": "strict-origin-when-cross-origin",
    "Permissions-Policy": "geolocation=(), microphone=(), camera=()",
}


def apply():
    _orig = RequestHandler.finish

    def _secure_finish(self, chunk=None):
        for name, value in _HEADERS.items():
            self.set_header(name, value)
        _orig(self, chunk)

    RequestHandler.finish = _secure_finish
