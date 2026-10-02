from __future__ import annotations
import os, uuid
from pathlib import Path
from ..legacy import SolarMissionControl, VERSION
from ..storage.database import Database
from ..reports.pdf_report import build_pdf
from ..visualization.interactive import build_interactive_timeline
from ..notifications.webhook import send_webhook

class Application:
 def __init__(self,config): self.config=config
 def run(self,quick=False,pdf=False,interactive=False,alert=False,dry_run=False):
  cfg=self.config; out=cfg['application']['output_directory']; run_id=str(uuid.uuid4())
  db=Database(cfg['storage']['database_url']) if cfg['storage']['enabled'] else None
  if db: db.start_run(run_id,'3.0.0',out)
  app=SolarMissionControl(output_dir=out,with_plots=cfg['visuals']['enabled'],with_images=cfg['visuals']['include_images'],write_html=cfg['reports']['html'])
  status='complete'; warnings=[]
  try:
   classification=app.run(quick_check=quick,hours_back=cfg['analysis']['hours_back'],hours_forward=cfg['analysis']['hours_forward'])
   report=app.report_generator.generate_full_report() if not quick else app.report_generator.generate_quick_check()
   vis=app.visualizer
   pdf_path=None
   if pdf and vis:
    pdf_path=build_pdf(report,vis.figures,vis.images,str(Path(out)/'solar_mission_control_report.pdf'))
   interactive_path=None
   if interactive:
    rows=app.aggregator.build_risk_timeline(cfg['analysis']['hours_back'],cfg['analysis']['hours_forward'],cfg['analysis']['risk_step_hours'])
    interactive_path=build_interactive_timeline(rows,str(Path(out)/'interactive_risk_timeline.html'))
   conditions,risk=app.report_generator._risk_inputs(); outlook=app.aggregator.get_forecast_outlook()
   payload={'version':'3.0.0','run_id':run_id,'current_level':risk['level'],'current_score':risk['overall_risk'],'forecast_level':outlook['level'],'peak_forecast_kp':outlook['peak_kp'],'classification':classification,'report_path':str(Path(out)/'index.html')}
   notification=send_webhook(payload,dry_run=dry_run) if alert else None
   return {'run_id':run_id,'classification':classification,'pdf':pdf_path,'interactive':interactive_path,'notification':notification}
  except Exception as e:
   status='failed';warnings.append(f'{type(e).__name__}: {e}');raise
  finally:
   if db:db.end_run(run_id,status,warnings)
