from __future__ import annotations
import sqlite3, json
from pathlib import Path
from datetime import datetime, timezone

SCHEMA='''CREATE TABLE IF NOT EXISTS runs(id TEXT PRIMARY KEY,started_at TEXT,ended_at TEXT,status TEXT,version TEXT,output_dir TEXT,warnings TEXT);
CREATE TABLE IF NOT EXISTS notifications(fingerprint TEXT PRIMARY KEY,sent_at TEXT,level TEXT,payload TEXT);
CREATE TABLE IF NOT EXISTS cme_arrivals(event_id TEXT,modeled TEXT,observed TEXT,residual_hours REAL,source TEXT);'''
class Database:
 def __init__(self,url):
  path=url.replace('sqlite:///',''); Path(path).parent.mkdir(parents=True,exist_ok=True); self.path=path
  with self.connect() as c: c.executescript(SCHEMA)
 def connect(self): return sqlite3.connect(self.path)
 def start_run(self,run_id,version,out):
  with self.connect() as c:c.execute('INSERT OR REPLACE INTO runs VALUES(?,?,?,?,?,?,?)',(run_id,datetime.now(timezone.utc).isoformat(),None,'running',version,out,'[]'))
 def end_run(self,run_id,status='complete',warnings=None):
  with self.connect() as c:c.execute('UPDATE runs SET ended_at=?,status=?,warnings=? WHERE id=?',(datetime.now(timezone.utc).isoformat(),status,json.dumps(warnings or []),run_id))
