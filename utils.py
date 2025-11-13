import rasterio
from pyproj import Transformer
import matplotlib.pyplot as plt
import sys


def show_geotiff(tif_path):
    with rasterio.open(tif_path) as src:
        img = src.read(1)
        transform = src.transform

        fig, ax = plt.subplots()
        im = ax.imshow(img, cmap='gray')
        plt.colorbar(im)

        clicked_coords = []
        def onclick(event):
            if event.inaxes != ax:
                return
            x_pix, y_pix = int(event.xdata), int(event.ydata)
            val = img[y_pix, x_pix]
            x, y = rasterio.transform.xy(transform, y_pix, x_pix)
            to_wgs84 = Transformer.from_crs(src.crs, "EPSG:4326", always_xy=True)
            lon, lat = to_wgs84.transform(x, y)

            clicked_coords.append((x, y, lon, lat, val))
            plt.close(fig)

        cid = fig.canvas.mpl_connect('button_press_event', onclick)
        plt.show()

        if clicked_coords:
            return clicked_coords[0]
        else:
            return None

if __name__ == "__main__":
    """ 
        Usage: python utils.py <path_to_geotiff>. 
        E.g python utils.py S2B_MSIL2A_20250107T051119_N0511_R019_T43QHU_20250107T080132_green.tif
    """
    x, y, lon, lat, val = show_geotiff(sys.argv[1])
    print(f"X: {x}, Y: {y}, latitude: {lat}, longitude: {lon}, Pixel Value: {val}")
