import rasterio
from rasterio.features import geometry_mask
import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt


def normalize_image(img):
    p2, p98 = np.percentile(img,  (2, 98))
    img_stretched = np.clip(img, p2, p98)
    return (img_stretched - p2) / (p98 - p2)


def show_green_nir(green, nir):
    green_norm = normalize_image(green)
    nir_norm = normalize_image(nir)

    fig, axs = plt.subplots(2, 1, figsize=(12, 6), sharex=True, sharey=True)

    axs[0].imshow(green_norm, cmap="gray")
    axs[0].set_title("Green Band")
    axs[1].imshow(nir_norm, cmap="gray")
    axs[1].set_title("NIR Band")

    plt.tight_layout()
    plt.show()


def crop_to_aoi(image, aoi_proj, transform):
    mask = geometry_mask(
        [geom for geom in aoi_proj.geometry],
        transform=transform,
        invert=True,  # invert=True means mask is True *inside* polygon
        out_shape=image.shape,
    )
    masked_image = np.where(mask, image, 0)
    rows = np.any(masked_image != 0, axis=1)
    cols = np.any(masked_image != 0, axis=0)

    row_min, row_max = np.where(rows)[0][[0, -1]]
    col_min, col_max = np.where(cols)[0][[0, -1]]

    return masked_image[row_min:row_max+1, col_min:col_max+1]


def main(green_path, nir_path, aoi_path):
    gdf = gpd.read_file(aoi_path)
    aoi_gdf = gpd.GeoDataFrame(geometry=[gdf.geometry[0]], crs=gdf.crs)
    with rasterio.open(green_path) as gsrc, rasterio.open(nir_path) as nsrc:
        aoi_proj = aoi_gdf.to_crs(gsrc.crs)
        green = gsrc.read(1).astype(np.float32)
        nir = nsrc.read(1).astype(np.float32)
        green_crop = crop_to_aoi(green, aoi_proj, gsrc.transform)
        nir_crop = crop_to_aoi(nir, aoi_proj, nsrc.transform)

    show_green_nir(green_crop, nir_crop)
    # show_green_nir(green, nir)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Denoising examples for S2 data")
    parser.add_argument(
        "-g",
        "--green",
        type=str,
        required=True,
        help="Path to the location where the green band is stored as geotiff file",
    )
    parser.add_argument(
        "-n",
        "--nir",
        type=str,
        required=True,
        help="Path to the location where the nir band is stored as geotiff file",
    )
    parser.add_argument(
        "-a",
        "--aoi-path",
        type=str,
        required=True,
        help="Path to the location where the aoi geojson is located"
    )
    args = parser.parse_args()

    main(args.green, args.nir, args.aoi_path)
