import json
from urllib.request import urlopen
from pathlib import Path

Path("data/geo").mkdir(parents=True, exist_ok=True)
url = (
    "https://raw.githubusercontent.com/codeforamerica/click_that_hood"
    "/master/public/data/brazil-states.geojson"
)
with urlopen(url) as resp:
    geojson = json.load(resp)
with open("data/geo/brazil-states.geojson", "w", encoding="utf-8") as f:
    json.dump(geojson, f, ensure_ascii=False)
print(f"Features: {len(geojson['features'])}")
# Check sigla property
siglas = [feat["properties"]["sigla"] for feat in geojson["features"]]
print(f"Ex sigla: {siglas[0]}")
assert len(geojson["features"]) == 27, f"Expected 27 states, got {len(geojson['features'])}"
assert "SP" in siglas, "SP not found"
print("GeoJSON OK")
