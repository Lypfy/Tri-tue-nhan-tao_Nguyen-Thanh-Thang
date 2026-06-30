import urllib.request
import json
import math

url = 'https://gist.githubusercontent.com/hoanganh25991/00e8f0162e41ac31ecd7/raw/bddd481d798c1777e6eae2a60443ac15a3178125/district-boundary-hcm-city.geojson'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
resp = urllib.request.urlopen(req)
data = json.loads(resp.read().decode('utf-8'))

# Mappings from geojson properties to our HCMC_DISTRICTS
NAME_MAPPING = {
    "District 1": "Quận 1",
    "District 2": "Thủ Đức",
    "District 3": "Quận 3",
    "District 4": "Quận 4",
    "District 5": "Quận 5",
    "District 6": "Quận 6",
    "District 7": "Quận 7",
    "District 8": "Quận 8",
    "District 9": "Thủ Đức",
    "District 10": "Quận 10",
    "District 11": "Quận 11",
    "District 12": "Quận 12",
    "Binh Tan": "Bình Tân",
    "Binh Thanh": "Bình Thạnh",
    "Go Vap": "Gò Vấp",
    "Phu Nhuan": "Phú Nhuận",
    "Tan Binh": "Tân Bình",
    "Tan Phu": "Tân Phú",
    "Thu Duc": "Thủ Đức",
    "Binh Chanh": "Bình Chánh",
    "Can Gio": "Cần Giờ",
    "Cu Chi": "Củ Chi",
    "Hoc Mon": "Hóc Môn",
    "Nha Be": "Nhà Bè"
}

min_lon = float('inf')
max_lon = float('-inf')
min_lat = float('inf')
max_lat = float('-inf')

raw_polygons = {}

for feature in data.get('features', []):
    props = feature.get('properties', {})
    # Check what the name field is
    name = props.get('name') or props.get('NAME_2') or props.get('Name') or props.get('TEN_HUYEN')
    if not name:
        continue
    
    # Try to map the name to our format
    mapped_name = None
    for k, v in NAME_MAPPING.items():
        if k.lower() in name.lower():
            mapped_name = v
            break
            
    if not mapped_name:
        # Check if name is like "Quận 1"
        if "quận" in name.lower() or "quan" in name.lower():
            mapped_name = name
        else:
            mapped_name = name
    
    geom = feature.get('geometry', {})
    geom_type = geom.get('type')
    coords = geom.get('coordinates', [])
    
    polys = []
    if geom_type == 'Polygon':
        polys = [coords[0]] # Just take the exterior ring
    elif geom_type == 'MultiPolygon':
        # Just take the exterior ring of the largest polygon
        largest_poly = max(coords, key=lambda p: len(p[0]))
        polys = [largest_poly[0]]
        
    for poly in polys:
        for lon, lat in poly:
            min_lon = min(min_lon, lon)
            max_lon = max(max_lon, lon)
            min_lat = min(min_lat, lat)
            max_lat = max(max_lat, lat)
            
    if mapped_name not in raw_polygons:
        raw_polygons[mapped_name] = []
    raw_polygons[mapped_name].extend(polys)

# Normalize
normalized_polygons = {}
lon_range = max_lon - min_lon
lat_range = max_lat - min_lat

for name, polys in raw_polygons.items():
    norm_polys = []
    # Since we want a single polygon for simple canvas drawing, we might have multiple rings (e.g. Thu Duc is made of D2, D9, Thu Duc).
    # For UI simplicity we just draw them as separate polygons or flatten them.
    # We will just save a list of points per district. If a district has multiple polygons, we insert None or handle it.
    # Actually, canvas.create_polygon can take multiple points but draws one continuous shape.
    # To draw MultiPolygons cleanly without crossing lines, we can just save a list of lists.
    # Let's save it as a list of points and let ui.py handle it, or just merge them naively.
    
    # Better: return a list of polygons per district: List[List[Point]]
    
    for poly in polys:
        n_poly = []
        for lon, lat in poly:
            nx = (lon - min_lon) / lon_range
            # Latitude is inverted (y goes down on screen)
            ny = 1.0 - (lat - min_lat) / lat_range
            n_poly.append((nx, ny))
        norm_polys.append(n_poly)
    
    # To keep compatible with current UI which expects a single list of (x,y)
    # If there are multiple polys, we can either update UI to handle List[List] or just concatenate.
    # Let's just concatenate them for now, it might have one crossing line but that's okay, 
    # or we can update the UI to loop over shapes. Let's just update the structure to be List[List[(x,y)]]
    normalized_polygons[name] = norm_polys

# Write back to map_data.py
with open("algorithms/csp/map_data.py", "w", encoding="utf-8") as f:
    f.write("DISTRICT_POLYGONS = " + json.dumps(normalized_polygons, indent=4, ensure_ascii=False) + "\n")

print("Successfully downloaded and processed GeoJSON!")
