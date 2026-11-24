from fastmcp import FastMCP
from core import grants,accessibility
mcp=FastMCP("MUHRIS GrantScout and AccessMap")
@mcp.tool
def discover_us_funding(keyword: str)->dict:
    """Discover US Grants.gov public opportunities; eligibility is not decided."""
    return grants(keyword)
@mcp.tool
def inspect_mapped_accessibility(latitude:float,longitude:float)->dict:
    """Read crowd-sourced wheelchair-access tags in a 1.5km area."""
    return accessibility(f"{latitude},{longitude}")
if __name__=="__main__":mcp.run()
