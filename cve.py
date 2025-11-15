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
    #print(f"Found {len(all_cves)} CVEs mentioning '{product_name}' in the last 365 days.\n")
    #print(all_cves[0])
    product_risk=0
    n=len(all_cves)
    for item in all_cves:
        cve_id = item["cve"]["id"]
        description = item["cve"]["descriptions"][0]["value"]
        base_score = item["cve"]["metrics"]["cvssMetricV31"][0]["cvssData"]["baseScore"]
        base_severity = item["cve"]["metrics"]["cvssMetricV31"][0]["cvssData"]["baseSeverity"]
        exploitabilityScore = item["cve"]["metrics"]["cvssMetricV31"][0]["exploitabilityScore"]
        impactScore = item["cve"]["metrics"]["cvssMetricV31"][0]["impactScore"]
        vulnStatus = item["cve"]["vulnStatus"]
        status_penalty = 0 if vulnStatus == "Analyzed" else 0.05 if vulnStatus == "Awaiting analysis" else -0.2
        badness = (0.55*exploitabilityScore/10)+(0.4*impactScore/10)+status_penalty
        severity_weight = 2.5 if base_severity == "CRITICAL" else 1.5 if base_severity == "HIGH" else 1.0 if base_severity == "MEDIUM" else 0.5 
        product_risk += badness*severity_weight
        results.append({
            "cve_id": cve_id,
            "description": description,
            "base_score": base_score,
            "base_severity": base_severity,
            "vulnStatus": vulnStatus,
            "exploitabilityScore": exploitabilityScore,
            "impactScore": impactScore
        })
        #print(f"{cve_id}: {description} CVSS score: {base_score} CVSS Severity {base_severity}\n")

    max_risk = n*1.5*2.5
    trust_score = 100 - (product_risk/max_risk)*100
    # --- Final JSON ---
    output = {
        "product": product_name,
        "trust_score": trust_score,
        "data": results
    }
    return output
    #print(output)

#get_cve_records_by_keyword(product_name="Zoom", use_exact_match=False)