import pandas as pd
import plotly.express as px
import colorsys
from pathlib import Path


file_path = r"C:\Users\apatil\Desktop\Energy-LDRD\Website\Figure2Data.xlsx"
df = pd.read_excel(file_path)


df_agg = (
    df.groupby("Category", as_index=False)["Data"]
      .sum()
)


df_agg = df_agg[df_agg["Data"] > 0].copy()
df_agg = df_agg.sort_values("Data", ascending=False).reset_index(drop=True)


total = df_agg["Data"].sum()
df_agg["Share_pct"] = 100 * df_agg["Data"] / total
df_agg["Category_clean"] = df_agg["Category"].astype(str).str.replace("_", " ", regex=False)


df_agg["Display_text"] = df_agg.apply(
    lambda r: f"<b>{r['Category_clean']}</b><br>{r['Share_pct']:.1f}%"
    if r["Share_pct"] >= 1 else "",
    axis=1
)


def generate_distinct_colors(n, s=0.65, v=0.80):
    colors = []
    golden_ratio = 0.61803398875
    h = 0.11
    for _ in range(n):
        h = (h + golden_ratio) % 1
        r, g, b = colorsys.hsv_to_rgb(h, s, v)
        colors.append("#{0:02X}{1:02X}{2:02X}".format(
            int(r * 255), int(g * 255), int(b * 255)
        ))
    return colors


categories = df_agg["Category_clean"].unique()
palette = generate_distinct_colors(len(categories))
color_map = dict(zip(categories, palette))


fig = px.treemap(
    df_agg,
    path=["Category_clean"],
    values="Data",
    color="Category_clean",
    color_discrete_map=color_map,
    custom_data=["Share_pct", "Data", "Display_text"]
)


fig.update_traces(
    texttemplate="%{customdata[2]}",
    textfont_size=20,
    marker=dict(line=dict(color="white", width=2), cornerradius=5),
    tiling=dict(pad=3),
    hovertemplate=(
        "<b>%{label}</b><br>"
        "Value: %{customdata[1]:.3f}<br>"
        "Share: %{customdata[0]:.2f}%"
        "<extra></extra>"
    )
)


fig.update_layout(
    title=dict(text="Unit Operation Level 2", x=0.5),
    paper_bgcolor="white",
    margin=dict(t=70, l=10, r=10, b=10)
)


output_file = Path(r"C:\Users\apatil\Desktop\Energy-LDRD\Website\chart2.html")
fig.write_html(str(output_file), full_html=True)


print("Saved to:", output_file)
print("File exists:", output_file.exists())