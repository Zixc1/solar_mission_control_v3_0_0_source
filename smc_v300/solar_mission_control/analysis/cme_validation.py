import numpy as np

def validation_metrics(pairs):
    residuals=np.array([(o-m).total_seconds()/3600 for m,o in pairs],dtype=float)
    if not len(residuals):return {}
    return {'count':len(residuals),'mae_hours':float(np.mean(np.abs(residuals))),'rmse_hours':float(np.sqrt(np.mean(residuals**2))),'median_ae_hours':float(np.median(np.abs(residuals))),'bias_hours':float(np.mean(residuals))}
