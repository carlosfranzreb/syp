from ipaddress import ip_address
from datetime import datetime as dt
from flask import request

from syp.models.gdpr_consents import GDPR
from syp import db


def save_cookies_consent(accepts):
    """ Saves user response to ge cookie banner. """
    ip = int(ip_address(request.remote_addr))
    consent = GDPR.query.filter_by(ip=ip).first()
    if consent is not None:
        consent.has_consented = accepts
        consent.asked_at = dt.now()
    else:
        db.session.add(GDPR(
            ip=ip,
            has_consented=accepts
        ))
    db.session.commit()
