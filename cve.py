import requests
import time
from datetime import datetime, timedelta, timezone
from urllib.parse import quote_plus

def get_cve_records_by_keyword(product_name,use_exact_match):
    # === Compute date range (last 365 days) ===
    # === Compute date range (last 120 days maximum per API limit) ===
    end_date = datetime.now(timezone.utc)
    start_date = end_date - timedelta(days=119)  # NVD max 120-day range
    pub_start = start_date.strftime("%Y-%m-%dT00:00:00.000Z")
    pub_end = end_date.strftime("%Y-%m-%dT23:59:59.999Z")


    headers = {}

    # === Encode keyword search ===
    keyword = quote_plus(product_name)  # URL-encode spaces
    params = {
        "keywordSearch": keyword,
        "pubStartDate": pub_start,
        "pubEndDate": pub_end,
        "startIndex": 0,
        "resultsPerPage": 2000  # Max results per page
    }

    # Add keywordExactMatch flag if needed
    if use_exact_match:
        params["keywordExactMatch"] = ""
    
    all_cves = []
    results = []

    # === Pagination loop ===
    while True:
        response = requests.get("https://services.nvd.nist.gov/rest/json/cves/2.0", params=params, headers=headers)
        response.raise_for_status()
        data = response.json()

        vulnerabilities = data.get("vulnerabilities", [])
        all_cves.extend(vulnerabilities)

        total_results = data.get("totalResults", 0)
        next_index = params["startIndex"] + params["resultsPerPage"]
        if next_index >= total_results:
            break

        # Prepare next page
        params["startIndex"] = next_index
        time.sleep(6)  # Respect NVD rate limits

    # === Output results ===
    print(f"Found {len(all_cves)} CVEs mentioning '{product_name}' in the last 365 days.\n")
    for item in all_cves:
        cve_id = item["cve"]["id"]
        description = item["cve"]["descriptions"][0]["value"]
        base_score = item["cve"]["metrics"]["cvssMetricV31"][0]["cvssData"]["baseScore"]
        base_severity = item["cve"]["metrics"]["cvssMetricV31"][0]["cvssData"]["baseSeverity"]
        results.append({
            "cve_id": cve_id,
            "description": description,
            "base_score": base_score,
            "base_severity": base_severity
        })
        #print(f"{cve_id}: {description} CVSS score: {base_score} CVSS Severity {base_severity}\n")
    # --- Build summary counts ---
    summary = {
        "critical": sum(1 for r in results if r["base_severity"].upper() == "CRITICAL"),
        "high":     sum(1 for r in results if r["base_severity"].upper() == "HIGH"),
        "medium":   sum(1 for r in results if r["base_severity"].upper() == "MEDIUM"),
        "low":      sum(1 for r in results if r["base_severity"].upper() == "LOW")
    }

    # --- Final JSON ---
    output = {
        "product": product_name,
        "summary": summary,
        "data": results
    }
    return output
    #print(output)

#get_cve_records_by_keyword(product_name="Zoom", use_exact_match=False)