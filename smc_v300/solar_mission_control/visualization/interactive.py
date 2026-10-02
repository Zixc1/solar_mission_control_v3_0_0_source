def build_interactive_timeline(rows,output_path):
    try: import plotly.graph_objects as go
    except ImportError:return None
    fig=go.Figure()
    for key in ('composite','xray','proton','geomagnetic','solar_wind'):
        valid=[r for r in rows if r.get(key) is not None]
        fig.add_trace(go.Scatter(x=[r['timestamp'] for r in valid],y=[r[key] for r in valid],mode='lines+markers',name=key.replace('_',' ').title()))
    fig.update_layout(title='Interactive Risk Timeline',yaxis_range=[0,100],template='plotly_white')
    fig.write_html(output_path,include_plotlyjs='cdn');return output_path
