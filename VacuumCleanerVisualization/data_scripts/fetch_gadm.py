"""
Tải dữ liệu GADM VNM Level 2 và xuất ra map_data.py cho TPHCM.
"""
import urllib.request
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

GADM_URL = "https://geodata.ucdavis.edu/gadm/gadm4.1/json/gadm41_VNM_2.json"

# Ánh xạ từ NAME_2 của GADM (không dấu cách) sang tên trong HCMC_DISTRICTS
NAME_MAP = {
    "Quận1": "Quận 1",
    "Quận3": "Quận 3",
    "Quận4": "Quận 4",
    "Quận5": "Quận 5",
    "Quận6": "Quận 6",
    "Quận7": "Quận 7",
    "Quận8": "Quận 8",
    "Quận10": "Quận 10",
    "Quận11": "Quận 11",
    "Quận12": "Quận 12",
    "BìnhThạnh": "Bình Thạnh",
    "GòVấp": "Gò Vấp",
    "PhúNhuận": "Phú Nhuận",
    "TânBình": "Tân Bình",
    "TânPhú": "Tân Phú",
    "BìnhTân": "Bình Tân",
    "ThànhPhốThủĐức": "Thủ Đức",
    "ThủĐức": "Thủ Đức",
    "NhàBè": "Nhà Bè",
    "HócMôn": "Hóc Môn",
    "CủChi": "Củ Chi",
    "BìnhChánh": "Bình Chánh",
    "CầnGiờ": "Cần Giờ",
}

print("Downloading GADM data...", flush=True)
req = urllib.request.Request(GADM_URL, headers={'User-Agent': 'Mozilla/5.0'})
resp = urllib.request.urlopen(req)
data = json.loads(resp.read().decode('utf-8'))
print(f"Done! Total features: {len(data['features'])}", flush=True)

# Lấy tất cả feature của TPHCM
hcmc_features = []
for feature in data['features']:
    props = feature.get('properties', {})
    if props.get('NAME_1', '') == 'HồChíMinh':
        district_name = props.get('NAME_2', '')
        hcmc_features.append((district_name, feature))

print(f"HCMC districts found: {len(hcmc_features)}")
for name, _ in hcmc_features:
    mapped = NAME_MAP.get(name, f"UNKNOWN: {name}")
    print(f"  '{name}' -> '{mapped}'")

# Tính bounding box cho TPHCM để normalize
min_lon = float('inf')
max_lon = float('-inf')
min_lat = float('inf')
max_lat = float('-inf')

def get_coords(geometry):
    """Lấy tất cả tọa độ từ một geometry (Polygon hoặc MultiPolygon)"""
    all_rings = []
    if geometry['type'] == 'Polygon':
        all_rings.append(geometry['coordinates'][0])
    elif geometry['type'] == 'MultiPolygon':
        for poly in geometry['coordinates']:
            all_rings.append(poly[0])
    return all_rings

for _, feature in hcmc_features:
    rings = get_coords(feature['geometry'])
    for ring in rings:
        for lon, lat in ring:
            min_lon = min(min_lon, lon)
            max_lon = max(max_lon, lon)
            min_lat = min(min_lat, lat)
            max_lat = max(max_lat, lat)

print(f"\nBounding box: lon [{min_lon:.4f}, {max_lon:.4f}], lat [{min_lat:.4f}, {max_lat:.4f}]")

lon_range = max_lon - min_lon
lat_range = max_lat - min_lat

# Sinh ra normalized polygons
normalized = {}
for district_name, feature in hcmc_features:
    mapped_name = NAME_MAP.get(district_name)
    if not mapped_name:
        print(f"  [SKIP] Unmapped: '{district_name}'")
        continue
    
    rings = get_coords(feature['geometry'])
    poly_list = []
    for ring in rings:
        norm_ring = []
        for lon, lat in ring:
            nx = (lon - min_lon) / lon_range
            ny = 1.0 - (lat - min_lat) / lat_range  # invert Y
            norm_ring.append([round(nx, 5), round(ny, 5)])
        poly_list.append(norm_ring)
    
    if mapped_name in normalized:
        # Merge (Thủ Đức có thể gộp từ nhiều quận cũ)
        normalized[mapped_name].extend(poly_list)
    else:
        normalized[mapped_name] = poly_list

print(f"\nMapped districts: {len(normalized)}")
missing = []
target_districts = [
    "Quận 1", "Quận 3", "Quận 4", "Quận 5", "Quận 6", "Quận 7",
    "Quận 8", "Quận 10", "Quận 11", "Quận 12", "Bình Thạnh",
    "Gò Vấp", "Phú Nhuận", "Tân Bình", "Tân Phú", "Bình Tân",
    "Thủ Đức", "Nhà Bè", "Hóc Môn", "Củ Chi", "Bình Chánh", "Cần Giờ"
]
for d in target_districts:
    if d not in normalized:
        missing.append(d)

if missing:
    print(f"Missing districts: {missing}")
else:
    print("All 22 districts found!")

# Ghi ra file map_data.py
with open("algorithms/csp/map_data.py", "w", encoding="utf-8") as f:
    f.write("DISTRICT_POLYGONS = " + json.dumps(normalized, indent=2, ensure_ascii=False) + "\n")

print("\nWritten to algorithms/csp/map_data.py")
