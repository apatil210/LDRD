import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from pathlib import Path

file_path = r"C:\Users\apatil\Desktop\Energy-LDRD\Website\Figure3Data.xlsx"
df = pd.read_excel(file_path)

value_cols = ["Electricity", "Fuel", "Steam"]

df_agg = (
    df.groupby("Category", as_index=False)[value_cols]
      .sum()
)

df_agg["Category_clean"] = df_agg["Category"].astype(str).str.replace("_", " ", regex=False)

df_agg = df_agg[(df_agg[value_cols] > 0).any(axis=1)].copy()

base_palette = [
    "#A000FF",
    "#00D000",
    "#E00060",
    "#C6E000",
    "#C07030",
    "#3C7CFF",
    "#00B0FF",
    "#00C0A0",
    "#FF8000",
    "#FF00AA",
]

categories = df_agg["Category_clean"].tolist()
n_cat = len(categories)

palette = (base_palette * ((n_cat // len(base_palette)) + 1))[:n_cat]
color_map = dict(zip(categories, palette))

def make_labels(df_in, value_col):
    total = df_in[value_col].sum()
    out = df_in.copy()
    out = out[out[value_col] > 0].copy()
    out["Share_pct"] = 100 * out[value_col] / total
    out["Display_text"] = out.apply(
        lambda r: f"<b>{r['Category_clean']}</b><br>{r['Share_pct']:.1f}%"
        if r["Share_pct"] >= 1 else "",
        axis=1
    )
    return out

elec_df = make_labels(df_agg, "Electricity")
fuel_df = make_labels(df_agg, "Fuel")
steam_df = make_labels(df_agg, "Steam")

fig = make_subplots(
    rows=1,
    cols=3,
    specs=[[{"type": "domain"}, {"type": "domain"}, {"type": "domain"}]],
    subplot_titles=("Electricity", "Fuel", "Steam")
)

common_textfont = dict(size=18, color="white")

fig.add_trace(
    go.Treemap(
        labels=elec_df["Category_clean"],
        parents=[""] * len(elec_df),
        values=elec_df["Electricity"],
        customdata=elec_df[["Share_pct", "Electricity", "Display_text"]].values,
        texttemplate="%{customdata[2]}",
        textfont=common_textfont,
        marker=dict(
            colors=[color_map[c] for c in elec_df["Category_clean"]],
            line=dict(color="white", width=2)
        ),
        tiling=dict(pad=3),
        hovertemplate=(
            "<b>%{label}</b><br>"
            "Value: %{customdata[1]:.3f}<br>"
            "Share: %{customdata[0]:.2f}%"
            "<extra></extra>"
        ),
        branchvalues="total",
        name="Electricity"
    ),
    row=1, col=1
)

fig.add_trace(
    go.Treemap(
        labels=fuel_df["Category_clean"],
        parents=[""] * len(fuel_df),
        values=fuel_df["Fuel"],
        customdata=fuel_df[["Share_pct", "Fuel", "Display_text"]].values,
        texttemplate="%{customdata[2]}",
        textfont=common_textfont,
        marker=dict(
            colors=[color_map[c] for c in fuel_df["Category_clean"]],
            line=dict(color="white", width=2)
        ),
        tiling=dict(pad=3),
        hovertemplate=(
            "<b>%{label}</b><br>"
            "Value: %{customdata[1]:.3f}<br>"
            "Share: %{customdata[0]:.2f}%"
            "<extra></extra>"
        ),
        branchvalues="total",
        name="Fuel"
    ),
    row=1, col=2
)

fig.add_trace(
    go.Treemap(
        labels=steam_df["Category_clean"],
        parents=[""] * len(steam_df),
        values=steam_df["Steam"],
        customdata=steam_df[["Share_pct", "Steam", "Display_text"]].values,
        texttemplate="%{customdata[2]}",
        textfont=common_textfont,
        marker=dict(
            colors=[color_map[c] for c in steam_df["Category_clean"]],
            line=dict(color="white", width=2)
        ),
        tiling=dict(pad=3),
        hovertemplate=(
            "<b>%{label}</b><br>"
            "Value: %{customdata[1]:.3f}<br>"
            "Share: %{customdata[0]:.2f}%"
            "<extra></extra>"
        ),
        branchvalues="total",
        name="Steam"
    ),
    row=1, col=3
)

fig.update_layout(
    title=dict(text="Unit Operation Level 2", x=0.5),
    paper_bgcolor="white",
    margin=dict(t=80, l=10, r=10, b=10)
)

output_file = Path(r"C:\Users\apatil\Desktop\Energy-LDRD\Website\chart3.html")
fig.write_html(str(output_file), full_html=True)

print("Saved to:", output_file)
print("File exists:", output_file.exists())