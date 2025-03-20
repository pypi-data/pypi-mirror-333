import numpy as np
from loguru import logger
import geopandas as gpd
from skimage.transform import resize
from shapely.geometry import Point
from rasterio.crs import CRS

from evotrain.models.loi.data.seasonality import day_of_year_cyclic_feats
from evotrain.v2 import lat_lon_to_unit_sphere
from evotrain.meteo import load_meteo_embeddings

def load_latlon(bounds, epsg, resolution=10, steps=5):
    """
    Returns a lat, lon feature from the given bounds/epsg.

    This provide a coarse (but relatively fast) approximation to generate
    lat lon layers for each pixel.

    'steps' specifies how many points per axis should be use to perform
    the mesh approximation of the canvas
    """

    xmin, ymin, xmax, ymax = bounds
    out_shape = (
        int(np.floor((ymax - ymin) / resolution)),
        int(np.floor((xmax - xmin) / resolution)),
    )

    xx = np.linspace(xmin + resolution / 2, xmax - resolution / 2, steps)
    yy = np.linspace(ymax - resolution / 2, ymin + resolution / 2, steps)

    xx = np.broadcast_to(xx, [steps, steps]).reshape(-1)
    yy = np.broadcast_to(yy, [steps, steps]).T.reshape(-1)

    points = [Point(x0, y0) for x0, y0 in zip(xx, yy)]

    gs = gpd.GeoSeries(points, crs=CRS.from_epsg(epsg))
    gs = gs.to_crs(epsg=4326)

    lon_mesh = gs.apply(lambda p: p.x).values.reshape((steps, steps))
    lat_mesh = gs.apply(lambda p: p.y).values.reshape((steps, steps))

    lon = resize(lon_mesh, out_shape, order=1, mode="edge")
    lat = resize(lat_mesh, out_shape, order=1, mode="edge")

    return np.stack([lat, lon], axis=0).astype(np.float32)


def get_feats_head(shape_X, epsg, bounds, date, model_config):
    """
    Generate the feature head for the model

    Args:
    - shape_X: shape of the input tensor
    - epsg: EPSG code of the input data
    - bounds: bounds of the input data
    - date: date of the input data
    - model_config: model configuration

    Returns:
    - feats_head: feature head for the model
    """

    resolution = model_config["data_config"]["resolution"]
    try:
        year = int(str(date)[:4])
    except Exception as e:
        logger.error(f"Error in extracting year from date: {date}, {e}")

    feats_head = []
    if "meteo" in model_config["dl_model_config"]["bands_head"]:

        logger.info("Loading meteo embeddings")
        meteo_emb = load_meteo_embeddings(
            bounds, epsg, year, bounds_buffer=3000, order=2, resolution=resolution
        )
        logger.debug(f"Meteo embeddings loaded with shape: {meteo_emb.shape}")

        meteo_emb /= 250
        logger.debug("Meteo embeddings scaled to 0-1 range")
        feats_head.append(meteo_emb)

    if "latlon" in model_config["dl_model_config"]["bands_head"]:

        logger.info("Loading latlon and converting to unit sphere (x,y,z)")
        lat, lon = load_latlon(bounds, epsg, resolution=resolution)
        xx, yy, zz = lat_lon_to_unit_sphere(lat, lon)
        logger.debug("Latlon converted to unit sphere")

        xx = np.full((1, shape_X[1], shape_X[2]), xx)
        yy = np.full((1, shape_X[1], shape_X[2]), yy)
        zz = np.full((1, shape_X[1], shape_X[2]), zz)
        logger.debug(
            f"Unit sphere arrays created with shapes: {xx.shape}, {yy.shape}, {zz.shape}"
        )
        feats_head.append(xx)
        feats_head.append(yy)
        feats_head.append(zz)

    if "seasonal" in model_config["dl_model_config"]["bands_head"]:
        logger.info("Generating seasonal features")
        sin_cos = day_of_year_cyclic_feats(
            str(date), doy_jitter=0, height=shape_X[1], width=shape_X[2]
        )
        # Let's scale the sin_cos features to the range [0, 1]
        sin_cos = (sin_cos + 1) / 2
        logger.debug(f"Seasonal features generated with shape: {sin_cos.shape}")
        feats_head.append(sin_cos)

    feats_head = np.concatenate(feats_head, axis=0).astype(np.float32)
    logger.info(f"Feature head generated with shape: {feats_head.shape}")

    return feats_head
