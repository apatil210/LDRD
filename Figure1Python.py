import pandas as pd
import numpy as np
from matplotlib.colors import to_rgb, to_hex
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from pathlib import Path

base_color = "#474646"
light_factor = 0.001
file_path = r"C:\Users\apatil\Desktop\Energy-LDRD\Website\Figure1Data.xlsx"

def make_shades(base_color, n, light_factor=0.25):
    rgb = np.array(to_rgb(base_color))
    light_rgb = 1 - (1 - rgb) * light_factor
    return [
        to_hex(light_rgb + (rgb - light_rgb) * t)
        for t in np.linspace(1, 0, n)
    ]

df = pd.read_excel(file_path)

df_agg = (
    df.groupby("Category", as_index=False)["Data"]
      .sum()
)

df_agg = df_agg[df_agg["Data"] > 0].copy()
df_agg = df_agg.sort_values("Data", ascending=False).reset_index(drop=True)

categories = df_agg["Category"]
values = df_agg["Data"]
colors = make_shades(base_color, len(values), light_factor)

fig = make_subplots(
    rows=2, cols=1,
    shared_xaxes=True,
    row_heights=[0.15, 0.85],
    vertical_spacing=0.03
)

fig.add_trace(
    go.Bar(
        x=categories,
        y=values,
        marker=dict(color=colors, line=dict(color="black", width=1)),
        hovertemplate="%{x}<br>%{y:.1%}<extra></extra>"
    ),
    row=1, col=1
)

fig.add_trace(
    go.Bar(
        x=categories,
        y=values,
        marker=dict(color=colors, line=dict(color="black", width=1)),
        hovertemplate="%{x}<br>%{y:.1%}<extra></extra>"
    ),
    row=2, col=1
)

fig.update_yaxes(range=[0.19, 0.20], tickformat=".0%", row=1, col=1)
fig.update_yaxes(range=[0.00, 0.05], tickformat=".0%", row=2, col=1)

fig.update_xaxes(showticklabels=False, row=1, col=1)
fig.update_xaxes(showticklabels=False, row=2, col=1)

fig.update_layout(
    height=700,
    width=1200,
    showlegend=False,
    plot_bgcolor="white",
    paper_bgcolor="white",
    margin=dict(t=40, b=40, l=60, r=30)
)

output_file = Path(r"C:\Users\apatil\Desktop\Energy-LDRD\Website\chart1.html").resolve().parent / "chart1.html"
fig.write_html(output_file, full_html=True)

print("Saved to:", output_file)