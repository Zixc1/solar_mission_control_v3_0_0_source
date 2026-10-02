import json, os, hashlib, requests

def fingerprint(payload): return hashlib.sha256(json.dumps(payload,sort_keys=True).encode()).hexdigest()
def send_webhook(payload,dry_run=False,url=None,timeout=10):
    url=url or os.getenv('SPACE_WEATHER_WEBHOOK')
    if dry_run:return {'dry_run':True,'fingerprint':fingerprint(payload),'payload':payload}
    if not url:return {'skipped':'webhook not configured'}
    r=requests.post(url,json=payload,timeout=timeout); r.raise_for_status()
    return {'status':r.status_code,'fingerprint':fingerprint(payload)}
