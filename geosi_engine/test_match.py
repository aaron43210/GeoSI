import re
lowered = "calculate the vegetative index from the le07_l1tp_144054_20000128_20170213_01_t1_b4 and le07_l1tp_144054_20000128_20170213_01_t1_b5 satellite bands"
aliases = ["clip", "cut to", "crop", "extract", "subset", "shapefile from", "region from", "area from", "need", "get"]

for alias in aliases:
    if re.search(rf"\b{re.escape(alias)}\b", lowered):
        print(f"MATCHED: {alias}")
