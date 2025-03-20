from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
from sentinelhub import CRS, BBox, DataCollection, SHConfig
from sentinelhub import SentinelHubCatalog
import os
from dotenv import load_dotenv
import getpass
from pathlib import Path
import sys

USERNAME = getpass.getuser()

# Load environment variables from .env file
env_path = Path(f"/data/users/Private/{USERNAME}/configs/shub.env")
if env_path.exists():
    load_dotenv(env_path)
else:
    raise FileNotFoundError(f"The environment file {env_path} does not exist.")

# Your client credentials
sh_client_id = os.getenv("SH_CLIENT_ID")
sh_client_secret = os.getenv("SH_CLIENT_SECRET")

# Create a session
client = BackendApplicationClient(client_id=sh_client_id)
oauth = OAuth2Session(client=client)

# Get token for the session
token = oauth.fetch_token(
    token_url="https://services.sentinel-hub.com/auth/realms/main/protocol/openid-connect/token",
    client_secret=sh_client_secret,
    include_client_id=True,
)

# All requests using this session will have an access token automatically added
resp = oauth.get("https://services.sentinel-hub.com/configuration/v1/wms/instances")
print(resp.content)

args = sys.argv[1:]

if args and args[0] == "cdse":
    config = SHConfig()
    config.sh_client_id = "sh-b2657f43-6998-4c6b-9349-3710426365cb"
    config.sh_client_secret = "v2tFA0eACwXpsJKL8dls2foXaPweO0lJ"
    config.sh_base_url = "https://sh.dataspace.copernicus.eu"
    config.sh_token_url = "https://identity.dataspace.copernicus.eu/auth/realms/CDSE/protocol/openid-connect/token"
else:
    config = SHConfig(
        sh_client_id=sh_client_id,
        sh_client_secret=sh_client_secret,
    )
print(f"Config made: {config}")

catalog = SentinelHubCatalog(config=config)
catalog.get_info()
print(f"Catalog: {catalog}")

collections = catalog.get_collections()
collections = [
    collection
    for collection in collections
    if not collection["id"].startswith(("byoc", "batch"))
]
s2_coll = collections[2]
print(f"Sentinel 2 L2A collections: {s2_coll}")

time_interval = "2020-01-29", "2020-01-29"
caspian_sea_bbox = BBox((49.9604, 44.7176, 51.0481, 45.2324), crs=CRS.WGS84)
# bbox=BBox({"min_x": 0, "max_x": 180, "min_y": 0, "max_y": 180}, crs='UTM_60S'),


search_iterator = catalog.search(
    DataCollection.SENTINEL2_L2A,
    bbox=caspian_sea_bbox,
    time=time_interval,
    # filter="eo:cloud_cover > 90 AND platform = 'sentinel-2b'",
    filter="eo:cloud_cover > 90 ",
    fields={
        "include": [
            "id",
            "properties.datetime",
            "properties.eo:cloud_cover",
            "properties.platform",
            "properties.gsd",
            "properties.constellation",
            "properties.instruments",
            "properties.proj:epsg",
            "properties.proj:bbox",
            "properties.proj:geometry",
        ],
        "exclude": [],
    },  # CatalogItemSearchFieldsFields
)

"""
"properties": {
"datetime": "2020-12-29T10:18:19Z",
"platform": "sentinel-2b",
"instruments": [],
"constellation": "sentinel-2",
"gsd": 10,
"eo:cloud_cover": 93.93,
"proj:epsg": 32633,
"proj:bbox": [],
"proj:geometry": {}
},
"""

results = list(search_iterator)
print("Total number of results:", len(results))
for res in results:
    print(res.id)
