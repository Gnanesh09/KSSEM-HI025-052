# config.sh_client_id = "sh-aa8d9b0a-baee-4529-a2f0-9522341be14c"
# config.sh_client_secret = "h6Z0cN6ajXiNvF4FlwCCAANSnZidnAqz"

from sentinelhub import SentinelHubSession, SHConfig
from sentinelhub import (
    SHConfig, BBox, CRS, SentinelHubRequest, DataCollection, MimeType
)

# 🔧 Set up Sentinel Hub credentials
config = SHConfig()
config.sh_client_id =  "sh-b91c0f0e-b61d-4e02-90e8-fcb03342b0b8"
config.sh_client_secret = "3CHW3diqOXLoPjO4Kb4Lhx9kxnqoGL5A"
config.sh_base_url = "https://sh.dataspace.copernicus.eu"
config.sh_auth_base_url = "https://identity.dataspace.copernicus.eu/auth/realms/CDSE/protocol/openid-connect/token"



session = SentinelHubSession(config=config)
print("Access token:", session.token.access_token[:50], "...")

# # Define location (latitude, longitude)
# lat, lon = 13.5, 78.0  # Example location (India)
# bbox = BBox(bbox=[lon - 0.01, lat - 0.01, lon + 0.01, lat + 0.01], crs=CRS.WGS84)

# # Define NDVI evalscript
# evalscript = """
# //VERSION=3
# function setup() {
#   return {
#     input: ["B04", "B08", "dataMask"],
#     output: { bands: 1, sampleType: "FLOAT32" }
#   };
# }
# function evaluatePixel(samples) {
#   let red = samples.B04;
#   let nir = samples.B08;
#   return [(nir - red) / (nir + red)];
# }
# """

# # ✅ Proper SentinelHubRequest (new syntax)
# request = SentinelHubRequest(
#     evalscript=evalscript,
#     input_data=[
#         SentinelHubRequest.input_data(
#             data_collection=DataCollection.SENTINEL2_L2A,
#             time_interval=('2025-10-01', '2025-10-10')
#         )
#     ],
#     responses=[
#         SentinelHubRequest.output_response('default', MimeType.TIFF)
#     ],
#     bbox=bbox,
#     size=(100, 100),
#     config=config
# )

# # 🔍 Fetch data
# response = request.get_data()

# print("NDVI array shape:", len(response), "x", response[0].shape)
# print(response[0])
