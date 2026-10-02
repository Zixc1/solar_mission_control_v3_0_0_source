import argparse, json, time
from ..config.loader import load_config
from ..orchestration.application import Application

def parser():
 p=argparse.ArgumentParser(prog='solar-mission-control',description='Solar Mission Control v3.0.0')
 p.add_argument('command',nargs='?',default='run',choices=['run','quick','monitor','alert','health','validate-config','initialize-db'])
 p.add_argument('--config');p.add_argument('--output-dir');p.add_argument('--hours-back',type=int);p.add_argument('--hours-forward',type=int)
 p.add_argument('--pdf',action='store_true');p.add_argument('--interactive',action='store_true');p.add_argument('--dry-run',action='store_true');p.add_argument('--interval',type=int,default=15)
 p.add_argument('--no-images',action='store_true');p.add_argument('--no-plots',action='store_true');p.add_argument('--no-html',action='store_true')
 return p

def main(argv=None):
 args=parser().parse_args(argv);cfg=load_config(args.config)
 if args.output_dir:cfg['application']['output_directory']=args.output_dir
 if args.hours_back is not None:cfg['analysis']['hours_back']=args.hours_back
 if args.hours_forward is not None:cfg['analysis']['hours_forward']=args.hours_forward
 if args.no_images:cfg['visuals']['include_images']=False
 if args.no_plots:cfg['visuals']['enabled']=False
 if args.no_html:cfg['reports']['html']=False
 if args.command=='validate-config': print(json.dumps(cfg,indent=2));return
 if args.command=='health':
  mods={m:__import__('importlib').util.find_spec(m) is not None for m in ('numpy','matplotlib','PIL','astropy','sunpy','plotly','reportlab')};print(json.dumps(mods,indent=2));return
 app=Application(cfg)
 if args.command=='monitor':
  try:
   while True: print(json.dumps(app.run(pdf=args.pdf,interactive=args.interactive),indent=2,default=str));time.sleep(args.interval*60)
  except KeyboardInterrupt: return
 else: print(json.dumps(app.run(quick=args.command=='quick',pdf=args.pdf,interactive=args.interactive,alert=args.command=='alert',dry_run=args.dry_run),indent=2,default=str))
