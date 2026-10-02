from __future__ import annotations
from pathlib import Path

def build_pdf(text_report, figures, images, output_path):
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import getSampleStyleSheet
        from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Image,PageBreak,Preformatted
        from reportlab.lib.units import cm
    except ImportError:
        return None
    Path(output_path).parent.mkdir(parents=True,exist_ok=True)
    doc=SimpleDocTemplate(output_path,pagesize=A4,rightMargin=1.3*cm,leftMargin=1.3*cm,topMargin=1.2*cm,bottomMargin=1.2*cm)
    styles=getSampleStyleSheet(); story=[Paragraph('Solar Mission Control',styles['Title']),Spacer(1,12),Preformatted(text_report[:12000],styles['Code'])]
    for item in list(figures)+list(images):
        p=item.get('path')
        if not p or not Path(p).exists(): continue
        story += [PageBreak(),Paragraph(item.get('title','Plate'),styles['Heading2']),Image(p,width=18*cm,height=10.125*cm,kind='proportional'),Paragraph(item.get('caption',''),styles['BodyText'])]
    doc.build(story); return output_path
