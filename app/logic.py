from pathlib import Path
import rasterio
import numpy as np
import matplotlib.pyplot as plt
import ollama
import base64
import json
from chromadb import Client
from sentence_transformers import SentenceTransformer
import ollama, numpy as np
from LLM import METRIC_INFO, SYSTEM_PROMPT




# from LLM import mina_LLM

# path = '/content/drive/MyDrive/SkyDoc/' 
# zip_file = 'Capernicus/S2A_MSIL2A_20250501T100041_N0511_R122_T33TUJ_20250501T165013_SAFE.zip'
# path_to_zip_file = path + zip_file

SAFE_FOLDER = Path("/Users/amirrezadarvishzadeh/Desktop/SkyDoc/S2C_MSIL2A_20250512T100611_N0511_R022_T32SNJ_20250512T173114.SAFE")
# print(SAFE_FOLDER.exists())
granule_root = SAFE_FOLDER / "GRANULE"
granules = [g for g in granule_root.iterdir() if g.is_dir()]   # materialise the generator
# print("Granules found:", [g.name for g in granules])

IMG_FOLDER = next(SAFE_FOLDER.glob("GRANULE/L2A_T32SNJ_A003567_20250512T101118/IMG_DATA/R10m"))


def load_band(band_name):
  # IMG_FOLDER += Path(f"/{folder_name}")
  band_path = next(IMG_FOLDER.glob(f"*_{band_name}_10m.jp2"))
  with rasterio.open(band_path) as src:
    return src.read(1).astype(np.float32)

red = load_band("B04")
green = load_band("B03")
blue = load_band("B02")


def normalize(array):
  return (array - np.min(array)) / (np.max(array) - np.min(array))

rgb = np.dstack([normalize(red), normalize(green), normalize(blue)])

nir = load_band("B08")
ndvi = (nir - red) / (nir + red + 1e-6)

summary_capernicus = f"""
Satellite imagery analysis complete.
Average NDVI: {np.mean(ndvi):.2f}
Vegetation stress detected: {(ndvi < 0.3).mean()*100:.1f}%
Location: Florence region
Time: 2025-05-07

What emergency health recommendations do you have for this scenario?
"""
print(f'Average NDVI: {np.mean(ndvi):.2f}')


# raise 'hehe'

import georinex as gr

# hdr = gr.rinexheader("Galileo_data.rnx")   # just the text header
# print(hdr.keys())
# hdr.keys()


import georinex as gr
import pyproj

hdr = gr.rinexheader("/Users/amirrezadarvishzadeh/Desktop/SkyDoc/Galileo_data.rnx")

# 1.1  Most RINEX 3 headers give ECEF XYZ (metres)
#      hdr["position"] might be ('4885053.127', '783344.915', '4012044.108')
X, Y, Z = map(float, hdr["position"])

# 1.2  Convert ECEF → lat-lon-height (WGS-84)
ecef = pyproj.CRS.from_epsg(4978)
wgs84 = pyproj.CRS.from_epsg(4326)
lat, lon, h = pyproj.Transformer.from_crs(ecef, wgs84, always_xy=True).transform(X, Y, Z)
 
coordinates = (lat, lon)
print(coordinates)

copernicus_data = f'Average NDVI: {np.mean(ndvi):.2f} \n Vegetation stress detected: {(ndvi < 0.3).mean()*100:.1f}%'
Galileo_data = f'the coordinates from galileo satellite data {coordinates}'

### here you write your code: chatgpt

# vecdb   = Client().create_collection("session_store")   # lives in /tmp
# embedder = SentenceTransformer("all-MiniLM-L6-v2")

# context_chunks = [
#     f"Average NDVI for tile T32SNJ on 2025-05-07 is {ndvi.mean():.2f}.",
#     f"{(ndvi < 0.3).mean()*100:.1f}% of pixels indicate vegetation stress.",
#     f"GNSS location: {lat:.4f}°, {lon:.4f}°, height {h:.1f} m."
# ]

# for i, chunk in enumerate(context_chunks):
#     vecdb.add(f"chunk_{i}", embeddings=[embedder.encode(chunk)], documents=[chunk])



# prompt = 'Using ONLY the context above, propose **three** concrete SMART-Emergency-Healthcare solutions (tele-medicine, medical-logistics, or SAR-support) most relevant to this location and date.'

# query_vec = embedder.encode(prompt)
# ctx = vecdb.query(query_embeddings=[query_vec], n_results=3)['documents'][0]

# final_prompt = f"here is some information for you{METRIC_INFO}\n\n here are the metrics: {ctx}\n\nUser question: {prompt}"
# # print(f'here is the final prompt{final_prompt}')
# response = ollama.chat(model="gemma3:12b", messages=[{"role": "system", "content": SYSTEM_PROMPT},{"role":"user","content":final_prompt}])

# print(response['message']['content'])





def compute_scene_metrics():
    """
    Heavy Copernicus + Galileo processing.
    Returns a dict whose keys match those used in the prompt.
    """
    # ... Sentinel-2 reading, NDVI, Galileo conversion ...
    return {
        "acq_date":   "2025-05-07",
        "tile_id":    "T32SNJ",
        "lat":        lat,
        "lon":        lon,
        "height":     h,
        "avg_ndvi":   float(np.mean(ndvi)),
        "stress_pct": float((ndvi < 0.3).mean()*100),
        "sar_flag":   "No",
        "wx_summary": "hot and dry",
        "pop_density": 540
    }