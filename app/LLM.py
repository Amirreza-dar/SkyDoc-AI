import ollama
import base64
import json
from sentence_transformers import SentenceTransformer
from chromadb import Client
import ollama, json

# file_path = 'output_Rivacold.jsonl' # Replace with your file path
# data = read_jsonl_file(file_path)
# Now you can process the 'data' which is a list of dictionaries.
# For example, print the first dictionary:
# if data:
#  print(data[0]['text'])


# prompt = 'Here is the content of a jsonl file. I want you to extract the following information: find the selected option in every question. The format is as followed:  1 | 2 | 3 | 4 | 5 the answer is indicated by ✗ or X . for example: like : 1 2 3 4 ✗ or  1 | 2 | 3 | X | 5 .Here is the content of the file. I want you to write your response in the following this format: {q1: 1, q2: 3, q3: 4} and so on:'
# # json_file_content = data[0]['text'] 
# prompt_with_data = prompt + '\n' + json_file_content + '\n' + ' I want you to write your response in the following this format: question 1: 1 question 2: 3  and so on. and your response in english'

# ---------- 1. static system prompt ---------------------------------------
SYSTEM_PROMPT = """
You are an expert “Smart Emergency-Healthcare” adviser.
You excel at designing field-ready services that combine:
• Copernicus Sentinel-2 imagery and derived indices (NDVI, burn severity, flood extent)
• Galileo PNT & SAR signals (precise coordinates, distress-beacon data)
• Emerging IRIS² sat-com links for real-time telemetry
Your goal is to recommend practical, evidence-based solutions that improve access
to medical care for hard-to-reach or crisis-affected communities.
""".strip()

# ---------- 2. user-prompt template ---------------------------------------
METRIC_INFO = """
Acquisition date
    • Timestamp embedded in the Sentinel-2 product metadata (e.g., 2025-05-07T10:06:11Z).  
    • Shows how current the scene is so decisions aren’t based on out-of-date conditions.

Tile / scene ID
    • Sentinel tiling-grid code such as “T32SNJ”.  
    • Lets you re-download the exact granule, mosaic neighbours, or match to historical scenes.

Coordinates  (lat ° / lon ° / h m)
    • Derived from Galileo RINEX header → ECEF → WGS-84 conversion.  
    • Pinpoints the target area, enables DEM / weather look-ups, helps guide field teams.

Average NDVI
    • (NIR – Red) / (NIR + Red) using S-2 bands B08 & B04.  
    • Range −1 to +1; higher = healthier vegetation. Flags drought, burn scars, flood damage.

Vegetation-stress area (< 0.30 NDVI)
    • Percentage of pixels with NDVI below 0.30 (threshold adjustable).  
    • Rapid indicator of ecosystem stress; useful for triaging medical or food-aid deployment.

Distress beacon detected? (yes / no)
    • Boolean from Galileo SAR downlink; “yes” means a 406 MHz emergency beacon was heard.  
    • Direct cue that a person may need life-saving assistance.

Forecast (next 24 h)
    • Text summary pulled from a weather API at the scene’s coordinates.  
    • Guides heat-stress, hypothermia, flood-risk, and drone-flight planning.

Population density (people / km²)
    • Value from a gridded dataset such as GHSL or WorldPop.  
    • Estimates how many residents are affected; scales vaccine stock, tele-medicine bandwidth, etc.
"""

# ---------- 3. helper ------------------------------------------------------
def mina_LLM(data_dict, model="gemma3:12b"):
    """data_dict holds acq_date, tile_id, lat, lon, height, avg_ndvi …"""
    
    # user_prompt = USER_TMPL.format(**data_dict)
    user_prompt = data_dict
    
    response = ollama.chat(
        model=model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user",   "content": user_prompt}
        ]
    )
    return response["message"]["content"]




# def mina_LLM(prompt_with_data): 

#     response = ollama.chat(
#         model='gemma3:12b',
#         messages=[
#             {
#                 'role': 'user',
#                 'content': prompt_with_data,

#             }
#         ]
#     )
#     message = response['message']['content']
#     print(message)
#     return message



# 1. Embed and store authoritative docs once -------------------------------

