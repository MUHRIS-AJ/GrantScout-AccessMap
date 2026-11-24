# GrantScout + AccessMap · Funding and map data workflows

### GrantScout
Search public **US** grants via official [Grants.gov search2](https://www.grants.gov/api/api-guide). Query results show opportunity ID, agency, status and dates where supplied. **Does not calculate eligibility**, and does not cover Sri Lankan scholarships automatically.

```bash
python core.py GrantScout "research"
```

### AccessMap
Read public wheelchair-access tags near a coordinate using [OpenStreetMap / Overpass](https://wiki.openstreetmap.org/wiki/Overpass_API), without claiming the actual facility has been inspected.

```bash
python core.py AccessMap "6.9271,79.8612"
```

### Run UI, tests and MCP
```bash
python dashboard.py --port 8765
python -m unittest discover -s tests -v
pip install -r requirements.txt
python server.py
```
Local dashboard: http://localhost:8765. Optional remote MCP: `fastmcp run server.py:mcp --transport http --port 8000` (secure before exposing).

Specialists: discover public records → extract comparable fields → verify provenance and limitations → report. This is **a rule-based multi-stage prototype**, not autonomous AI.
