from axon.session import capture_inbound_headers, patch_requests

def instrument_with_axon(app, , app_name):
    @app.before_request
    def _capture_headers():
        from flask import request
        headers = dict(request.headers)
        headers["X-App-Name"] = app_name
        capture_inbound_headers(headers)
    
    patch_requests()
