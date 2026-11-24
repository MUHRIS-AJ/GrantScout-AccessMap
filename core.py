"""Grants.gov funding discovery and OpenStreetMap accessibility information."""
from __future__ import annotations
import re
from transport import request_json, SourceError

SERVICES = ["GrantScout","AccessMap"]
GRANTS="https://api.grants.gov/v1/api/search2"
OSM="https://overpass-api.de/api/interpreter"

def grants(keyword: str):
    if not isinstance(keyword,str) or not 2 <= len(keyword.strip()) <= 120:
        raise ValueError("Funding keyword must be 2–120 characters.")
    data=request_json(GRANTS,payload={"keyword":keyword.strip(),"rows":12,"oppStatuses":"posted|forecasted"})
    if data.get("errorcode",0) != 0:
        raise SourceError("Grants.gov returned: "+str(data.get("msg","API error")))
    hits=(data.get("data") or {}).get("oppHits") or []
    rows=[]
    for e in hits[:12]:
        key=e.get("id")
        if key is None: continue
        rows.append({"id":str(key),"title":e.get("title"),"number":e.get("number"),
                     "agency":e.get("agencyName"),"status":e.get("oppStatus"),
                     "open_date":e.get("openDate"),"close_date":e.get("closeDate"),
                     "source_url":"https://www.grants.gov/search-results-detail/"+str(key)})
    return {"project":"GrantScout","query":keyword,"count":len(rows),"opportunities":rows,
            "source":GRANTS,"agents":["Source: Grants.gov search2","Analysis: normalize dates and status",
            "Verification: funding ID and official link","Report: candidate list"],
            "limitations":["Grant eligibility and official deadlines are NOT independently evaluated.",
                           "Opportunity scope is US Grants.gov, not every country.",
                           "Verify the full opportunity notice before applying."]}

def accessibility(location: str):
    match=re.fullmatch(r"\s*(-?\d+(?:\.\d+)?),\s*(-?\d+(?:\.\d+)?)\s*",location)
    if not match:raise ValueError("Enter latitude,longitude (e.g. 6.9271,79.8612).")
    lat,lon=map(float,match.groups())
    if not -90<=lat<=90 or not -180<=lon<=180:raise ValueError("Coordinates out of range.")
    query=f'[out:json][timeout:15];nwr(around:1500,{lat:.5f},{lon:.5f})["wheelchair"];out center 25;'
    data=request_json(OSM,params={"data":query})
    rows=[]
    for e in (data.get("elements") or [])[:25]:
        tags=e.get("tags") or {}
        if not e.get("id"):continue
        rows.append({"name":tags.get("name") or "Unnamed place",
                     "wheelchair_tag":tags.get("wheelchair","unknown"),
                     "type":tags.get("amenity") or tags.get("shop") or tags.get("tourism") or "mapped feature",
                     "latitude":e.get("lat") or (e.get("center") or {}).get("lat"),
                     "longitude":e.get("lon") or (e.get("center") or {}).get("lon"),
                     "source_url":f'https://www.openstreetmap.org/{e.get("type","node")}/{e["id"]}',
                     "on_site_verified":False})
    return {"project":"AccessMap","location":location,"places":rows,"count":len(rows),
            "source":"OpenStreetMap via Overpass","agents":["Discover OSM wheelchair tags","Normalize mapped places",
            "Verify map provenance","Report mapped evidence"],
            "limitations":["Crowdsourced tags may be outdated, missing or incorrect.",
                           "Wheelchair tag alone does not establish complete accessibility.",
                           "No claims of on-site inspections or official certification."]}

def run(query: str,service: str="GrantScout"):
    if service=="GrantScout":return grants(query)
    if service=="AccessMap":return accessibility(query)
    raise ValueError("Unknown service.")
if __name__=="__main__":
    import argparse,json
    ap=argparse.ArgumentParser()
    ap.add_argument("service",choices=SERVICES);ap.add_argument("query")
    a=ap.parse_args()
    try:print(json.dumps(run(a.query,a.service),indent=2))
    except (ValueError,SourceError) as exc:ap.exit(2,str(exc)+"\n")
