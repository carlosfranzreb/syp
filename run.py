from ipaddress import ip_address
import datetime as dt
from flask import request
from syp import create_app
from syp.models.gdpr_consents import GDPR


app = create_app()


@app.context_processor
def accepts_cookies():
    """ Checks if the cookie banner must be shown, and if cookies
    can be installed. """
    ip = ip_address(request.remote_addr)
    consent = GDPR.query.filter_by(ip=int(ip)).first()
    if consent is None or not consent.has_consented and \
            consent.asked_at < dt.datetime.now() - dt.timedelta(days=30):
        return dict(cookies=None)
    return dict(cookies=consent.has_consented)

if __name__ == '__main__':
    app.run(debug=True)
