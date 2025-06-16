# utils.py

import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import LineString, Point
from shapely.errors import TopologicalError
import warnings

def plot_full_india_map(states_gdf):
    """Plot the full India map with state labels."""
    fig, ax = plt.subplots(figsize=(8, 10))
    states_gdf.boundary.plot(ax=ax, linewidth=0.8, edgecolor='black')
    states_gdf.plot(ax=ax, alpha=0.1)

    # Add labels
    for idx, row in states_gdf.iterrows():
        if row.geometry.is_empty or row.geometry.centroid.is_empty:
            continue
        point = row.geometry.centroid
        ax.text(point.x, point.y, row['State'], fontsize=7, ha='center')

    ax.axis('off')
    return fig


def draw_map_lines_with_labels(
    geo_data,
    selected_data,
    target_coords=None,
    line_style="Straight",
    label_field="State",
    show_boundaries=True
):
    """Draw map with optional lines and region labels."""
    fig, ax = plt.subplots(figsize=(8, 10))

    try:
        cleaned_geo = geo_data.copy()
        cleaned_geo['geometry'] = cleaned_geo['geometry'].buffer(0)  # Clean invalid geometries
    except TopologicalError:
        cleaned_geo = geo_data  # fallback

    # Plot background boundaries if toggled
    if show_boundaries:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            try:
                gpd.GeoSeries(cleaned_geo.unary_union.boundary).plot(ax=ax, linewidth=0.4, edgecolor='lightgray')
            except Exception:
                pass

    # Plot selected regions with darker color
    selected_data.plot(ax=ax, color='skyblue', edgecolor='black', linewidth=0.8)

    # Draw labels only for selected data
    for _, row in selected_data.iterrows():
        if row.geometry.is_empty:
            continue
        center = row.geometry.centroid
        label = row[label_field] if label_field in row else "Label"
        ax.text(center.x, center.y, label, fontsize=8, ha='center', weight='bold')

    # Draw lines if targets are given
    if target_coords and not selected_data.empty:
        for target in target_coords:
            for _, row in selected_data.iterrows():
                try:
                    centroid = row.geometry.centroid
                    line = LineString([centroid, Point(target)])
                    linestyle = '-' if line_style == "Straight" else '--' if line_style == "Dashed" else ':'
                    ax.plot(*line.xy, color='red', linestyle=linestyle)
                except Exception as e:
                    continue

    ax.axis('off')
    return fig
