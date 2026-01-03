import json
import re

# number and corresponding day of week
days_map = {
    0: "Monday",
    1: "Tuesday",
    2: "Wednesday",
    3: "Thursday",
    4: "Friday",
    5: "Saturday",
    6: "Sunday"
}

#bitmask values
SERVICE_VALUES = [
    1, 2, 4, 8, 16, 32, 64, 128, 256, 512,
    1024, 2048, 4096, 8192, 16384, 32768,
    65536, 131072, 262144, 524288, 1048576
]
PAY_METHOD_VALUES = [1, 2, 4, 8]

def add_seconds(time_str):
    """Adds :00 and makes sure of right format for xsd:time"""
    if not time_str:
        return time_str
    time_str = time_str.strip()
    match = re.match(r"^(\d{1,2}):(\d{1,2})(?::\d{1,2})?$", time_str)
    if match:
        h, m = match.group(1), match.group(2)
        return f"{int(h):02d}:{int(m):02d}:00"
    return time_str  # pokud už je ve správném formátu nebo jiný text


def parse_hours(hours_str, parent_id, from_id):
    """
    Splits following into 'opens' and 'closes' times and or makes a note about Lítačka hours:
    - "5:00-24:00"
    - "09:00-17:20 (Lítačka 09:00-17:00)"
    - "6:00-12:00,12:30-15:00"
    """
    result = {
        "intervals": []
    }

    if not hours_str:
        return result

    note_match = re.search(r"\((.*?)\)", hours_str)
    if note_match:
        result["note"] = note_match.group(1)
        hours_str = hours_str[:note_match.start()].strip()

    parts = [p.strip() for p in hours_str.split(",")]

    for part in parts:
        if "-" in part:
            start, end = part.split("-", 1)
            result["intervals"].append({
                "opens": add_seconds(start),
                "closes": add_seconds(end),
                "parentId": f"{parent_id}",
                "from": f"{from_id}"
            })

    return result


with open("pointsOfSale.json", "r", encoding="utf-8") as f:
    points_of_sale = json.load(f)

for point in points_of_sale:

    # --- OPENING HOURS ---
    for oh in point.get("openingHours", []):
        oh["parentId"] = point["id"]

        # transformations to day of week
        oh["from"] = days_map.get(oh["from"], oh["from"])
        oh["to"] = days_map.get(oh["to"], oh["to"])

        # parsing hours
        parsed = parse_hours(oh.get("hours"), oh.get("parentId"), oh.get("from"))
        oh["intervals"] = parsed.get("intervals", [])

        if "note" in parsed:
            oh["note"] = parsed["note"]

    # --- SERVICES bit mask ---
    services_mask = point.get("services")
    if services_mask is not None:
        point["servicesExpanded"] = [
            v for v in SERVICE_VALUES if services_mask & v
        ]

    # --- PAY METHODS bit mask ---
    pay_mask = point.get("payMethods")
    if pay_mask is not None:
        point["payMethodsExpanded"] = [
            v for v in PAY_METHOD_VALUES if pay_mask & v
        ]

with open("pointsOfSale_transformed.json", "w", encoding="utf-8") as f:
    json.dump(points_of_sale, f, ensure_ascii=False, indent=2)


