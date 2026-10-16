#!/usr/bin/env python3
"""Compare landscape frames using an airport boundary and runway geometry.

The geometry calculation uses UTM metres. Optional raster previews use an
explicit approximate registration; they are not orthorectified deliverables.
"""
import argparse
import hashlib
import json
import math
import os
from time import perf_counter
from pathlib import Path

os.environ.setdefault("MPLCONFIGDIR", "/tmp/kapa-matplotlib")
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from pyproj import Transformer


def polygon_area(points):
    centered = points - points[0]
    x, y = centered[:, 0], centered[:, 1]
    return abs(float(np.dot(x, np.roll(y, -1)) - np.dot(y, np.roll(x, -1)))) / 2


def make_frame(boundary, angle, aspect, margin):
    # Columns of basis are image-right and image-up in UTM coordinates.
    basis = np.array([[math.cos(angle), -math.sin(angle)],
                      [math.sin(angle), math.cos(angle)]])
    local = boundary @ basis
    low, high = local.min(axis=0), local.max(axis=0)
    center = (low + high) / 2
    required = (high - low) * (1 + 2 * margin)
    width = max(required[0], required[1] * aspect)
    height = width / aspect
    low = center - np.array([width, height]) / 2
    high = center + np.array([width, height]) / 2
    corners = np.array([[low[0], low[1]], [high[0], low[1]],
                        [high[0], high[1]], [low[0], high[1]], low]) @ basis.T
    assert np.all(local >= low - 1e-7) and np.all(local <= high + 1e-7)
    assert abs(width / height - aspect) < 1e-12
    return {"basis": basis, "low": low, "high": high, "corners": corners,
            "width_m": float(width), "height_m": float(height),
            "area_km2": float(width * height / 1e6),
            "airport_area_fraction": polygon_area(boundary) / (width * height),
            "image_right_bearing_deg": (90 - math.degrees(angle)) % 360,
            "all_boundary_vertices_inside": True}


def main():
    started = perf_counter()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-dir", type=Path, default=Path(__file__).resolve().parents[1] / "data/kapa_framing")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--image", type=Path)
    parser.add_argument("--aspect", type=float, default=1.5)
    parser.add_argument("--margin", type=float, default=0.1, help="Fraction added on each side before aspect fit")
    args = parser.parse_args()
    if args.aspect <= 1 or args.margin < 0:
        parser.error("Use a landscape aspect > 1 and a nonnegative margin")
    args.output.mkdir(parents=True, exist_ok=True)
    doc = json.loads((args.data_dir / "airport_geometry.geojson").read_text())
    project = Transformer.from_crs(4326, 32613, always_xy=True)
    inverse = Transformer.from_crs(32613, 4326, always_xy=True)

    def xy(coords):
        a = np.asarray(coords, dtype=float)
        return np.column_stack(project.transform(a[:, 0], a[:, 1]))

    airport = next(f for f in doc["features"] if f["properties"].get("icao") == "KAPA")
    boundary = xy(airport["geometry"]["coordinates"][0])
    runways = {f["properties"]["ref"]: xy(f["geometry"]["coordinates"])
               for f in doc["features"] if f["properties"].get("aeroway") == "runway"}
    main_runway = runways["17L/35R"]
    delta = main_runway[-1] - main_runway[0]
    angle = math.atan2(delta[1], delta[0])
    frames = {"north_up": make_frame(boundary, 0, args.aspect, args.margin),
              "runway_aligned": make_frame(boundary, angle, args.aspect, args.margin)}
    metrics = {"airport": "KAPA", "crs": "EPSG:32613 (WGS84 / UTM zone 13N)",
               "aspect_ratio": args.aspect, "margin_each_side_fraction": args.margin,
               "boundary_source": "OSM way 427832843; approximate mapped airport boundary, not a legal survey",
               "runway_length_m": {k: float(np.linalg.norm(v[-1] - v[0])) for k, v in runways.items()},
               "airport_area_km2": polygon_area(boundary) / 1e6, "frames": {}}
    features = []
    for name, f in frames.items():
        for runway in runways.values():
            local = runway @ f["basis"]
            assert np.all(local >= f["low"] - 1e-7) and np.all(local <= f["high"] + 1e-7)
        ll = np.column_stack(inverse.transform(f["corners"][:, 0], f["corners"][:, 1]))
        m = {k: v for k, v in f.items() if not isinstance(v, np.ndarray)}
        m["all_runway_vertices_inside"] = True
        m["lonlat_bbox"] = [float(ll[:, 0].min()), float(ll[:, 1].min()),
                            float(ll[:, 0].max()), float(ll[:, 1].max())]
        m["output_2400x1600_ground_m_per_pixel"] = f["width_m"] / 2400
        m["required_pixels_at_1m_gsd"] = [math.ceil(f["width_m"]), math.ceil(f["height_m"])]
        metrics["frames"][name] = m
        features.append({"type": "Feature", "properties": {"name": name, **m},
                         "geometry": {"type": "Polygon", "coordinates": [ll.tolist()]}})
    metrics["north_up_to_aligned_area_ratio"] = frames["north_up"]["area_km2"] / frames["runway_aligned"]["area_km2"]
    assert metrics["north_up_to_aligned_area_ratio"] > 1

    # This standalone geometry plot contains no source photograph.
    fig, ax = plt.subplots(figsize=(9, 9))
    origin = boundary.mean(axis=0)
    b = (boundary - origin) / 1000
    ax.fill(b[:, 0], b[:, 1], color="#c7e8c7", alpha=.7, label="Mapped airport boundary")
    for ref, line in runways.items():
        line = (line - origin) / 1000
        ax.plot(line[:, 0], line[:, 1], color="#444", linewidth=2)
        ax.text(*line.mean(axis=0), ref, fontsize=8)
    for name, color in [("north_up", "#2475b0"), ("runway_aligned", "#d45b21")]:
        c = (frames[name]["corners"] - origin) / 1000
        ax.plot(c[:, 0], c[:, 1], color=color, label=name.replace("_", " "))
    ax.set(aspect="equal", xlabel="East offset (km)", ylabel="North offset (km)",
           title="KAPA: same airport, two landscape frames (3:2; 10% each-side margin)")
    ax.grid(alpha=.2)
    ax.legend(loc="lower right")
    fig.text(.5, .015, "Boundary/runways: © OpenStreetMap contributors, ODbL 1.0 | Approximate planning geometry", ha="center", fontsize=8)
    fig.savefig(args.output / "frame_geometry.svg", bbox_inches="tight")
    fig.savefig(args.output / "frame_geometry.png", dpi=160, bbox_inches="tight")
    plt.close(fig)

    if args.image:
        reg = json.loads((args.data_dir / "registration.json").read_text())
        assert hashlib.sha256(args.image.read_bytes()).hexdigest() == reg["image_sha256"], "Unexpected source image"
        points = reg["control_points"]
        pixels = np.asarray([p["pixel"] for p in points], float)
        world = xy([p["lonlat"] for p in points])
        design = np.column_stack([pixels, np.ones(len(points))])
        coefficients, _, rank, _ = np.linalg.lstsq(design, world, rcond=None)
        assert rank == 3
        residuals = np.linalg.norm(design @ coefficients - world, axis=1)
        # Reserved points test the transform, instead of only reporting fit error.
        loo = []
        for i in range(len(points)):
            selected = np.arange(len(points)) != i
            model = np.linalg.lstsq(design[selected], world[selected], rcond=None)[0]
            loo.append(float(np.linalg.norm(design[i] @ model - world[i])))
        raster_matrix = coefficients[:2, :]
        raster_offset = coefficients[2, :]
        metrics["registration"] = {"method": reg["method"], "fit_rmse_m": float(np.sqrt(np.mean(residuals ** 2))),
                                   "max_fit_error_m": float(residuals.max()),
                                   "leave_one_out_errors_m": loo,
                                   "max_leave_one_out_error_m": max(loo),
                                   "source_sample_spacing_m": np.linalg.norm(raster_matrix, axis=1).tolist(),
                                   "source_reuse_license": "unconfirmed; local evaluation only",
                                   "geographic_accuracy": "Approximate manual registration; not certified georeferencing"}
        im = Image.open(args.image).convert("RGB")
        assert im.size == (reg["width_px"], reg["height_px"])
        fig, axes = plt.subplots(1, 2, figsize=(16, 6.6))
        for ax, (name, f) in zip(axes, frames.items()):
            out_w, out_h = 1800, 1200
            scale = np.diag([f["width_m"] / out_w, -f["height_m"] / out_h])
            pixel_to_world = scale @ f["basis"].T
            upper_left = np.array([f["low"][0], f["high"][1]]) @ f["basis"].T
            to_source = pixel_to_world @ np.linalg.inv(raster_matrix)
            offset = (upper_left - raster_offset) @ np.linalg.inv(raster_matrix)
            a = (to_source[0, 0], to_source[1, 0], offset[0],
                 to_source[0, 1], to_source[1, 1], offset[1])
            result = im.transform((out_w, out_h), Image.Transform.AFFINE, a,
                                  Image.Resampling.BICUBIC, fillcolor=(48, 52, 58))
            # Coverage is measured over the output frame. Missing source stays gray.
            mask = Image.new("L", im.size, 255).transform((out_w, out_h), Image.Transform.AFFINE,
                                                        a, Image.Resampling.NEAREST, fillcolor=0)
            coverage = float(np.asarray(mask).mean() / 255)
            metrics["frames"][name]["reference_raster_coverage_fraction"] = coverage
            result.save(args.output / (name + "_preview.jpg"), quality=94)
            ax.imshow(result)
            local = boundary @ f["basis"]
            bx = (local[:, 0] - f["low"][0]) / f["width_m"] * out_w
            by = (f["high"][1] - local[:, 1]) / f["height_m"] * out_h
            ax.plot(bx, by, color="#ffda36", linewidth=.8)
            north = np.array([0., 1.]) @ f["basis"]
            dx, dy = north[0] * 120, -north[1] * 120
            ax.annotate("N", xy=(170 + dx, 180 + dy), xytext=(170, 180), color="white",
                        fontsize=12, arrowprops={"arrowstyle": "->", "color": "white", "lw": 2})
            ax.set_title(f"{name.replace('_', ' ')}\n{f['width_m']/1000:.2f} × {f['height_m']/1000:.2f} km | source coverage {coverage:.0%}")
            ax.axis("off")
        fig.suptitle("KAPA framing experiment — same source photograph, two viewing frames", fontsize=14)
        fig.text(.5, .04, "Yellow: approximate OSM airport boundary | Gray: no source pixels, not fabricated scenery\n"
                 "Source: Centennial Airport aerial PDF; reuse permission unconfirmed. Local evaluation only.\n"
                 f"Approximate registration: fit RMSE {metrics['registration']['fit_rmse_m']:.0f} m; max held-out error {max(loo):.0f} m. Rotation adds no oblique view.", ha="center", fontsize=9)
        fig.tight_layout(rect=[0, .13, 1, .94])
        fig.savefig(args.output / "framing_comparison.png", dpi=160)
        plt.close(fig)
    metrics["limitations"] = ["Airport boundary is approximate OSM mapping, not surveyed property limits.",
                              "Frames specify ground coverage, not camera focal length or an oblique view.",
                              "Source photograph date, native GSD and commercial reuse permission are unconfirmed.",
                              "USGS/NAIP download and layer-specific reuse conditions have not been validated."]
    metrics["processing_seconds"] = round(perf_counter() - started, 3)
    (args.output / "metrics.json").write_text(json.dumps(metrics, indent=2) + "\n")
    (args.output / "frames.geojson").write_text(json.dumps({"type": "FeatureCollection", "features": features,
                                                          "attribution": doc["attribution"]}, indent=2) + "\n")
    print(json.dumps(metrics, indent=2))


if __name__ == "__main__":
    main()
