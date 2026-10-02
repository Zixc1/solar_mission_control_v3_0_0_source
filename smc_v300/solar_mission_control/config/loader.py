from __future__ import annotations
import json, os
from copy import deepcopy
from pathlib import Path

DEFAULTS = {
 'application': {'output_directory':'swrl_report','log_level':'INFO'},
 'analysis': {'hours_back':72,'hours_forward':48,'risk_step_hours':3},
 'visuals': {'enabled':True,'interactive':False,'width':2560,'height':1440,'dpi':200,'include_images':True},
 'reports': {'text':True,'html':True,'pdf':True,'interactive':False},
 'notifications': {'enabled':False,'threshold':'WATCH','cooldown_minutes':60},
 'storage': {'enabled':True,'database_url':'sqlite:///swrl_report/solar_mission_control.db','retention_days':180},
}

def _merge(a,b):
    out=deepcopy(a)
    for k,v in b.items(): out[k]=_merge(out.get(k,{}),v) if isinstance(v,dict) else v
    return out

def load_config(path=None):
    cfg=deepcopy(DEFAULTS)
    if path:
        text=Path(path).read_text(encoding='utf-8')
        if path.endswith(('.yaml','.yml')):
            import yaml; loaded=yaml.safe_load(text) or {}
        else: loaded=json.loads(text)
        cfg=_merge(cfg,loaded)
    env={'application':{'output_directory':os.getenv('SMC_OUTPUT_DIR',cfg['application']['output_directory'])}}
    cfg=_merge(cfg,env)
    validate_config(cfg)
    return cfg

def validate_config(c):
    assert c['analysis']['hours_back']>0
    assert c['analysis']['hours_forward']>=0
    assert c['visuals']['width']>0 and c['visuals']['height']>0 and c['visuals']['dpi']>0
    assert c['storage']['retention_days']>=1
    return c
