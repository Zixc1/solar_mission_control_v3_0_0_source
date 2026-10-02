from datetime import datetime,timezone,timedelta
from solar_mission_control.analysis.cme_validation import validation_metrics
from solar_mission_control.config.loader import load_config

def test_config(): assert load_config()['visuals']['width']==2560
def test_metrics():
 n=datetime.now(timezone.utc);m=validation_metrics([(n,n+timedelta(hours=2)),(n,n-timedelta(hours=2))])
 assert m['mae_hours']==2 and m['bias_hours']==0
