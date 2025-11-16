import requests
import os
import cve

def call_webhook_assess_product(product=None, company=None, sha1=None):
    """
    Sends a POST request with JSON content containing
    three parameters. Supports missing/None values.
    """
    print("call_webhook_assess_product ...\n")
    url = "https://plantbase.app.n8n.cloud/webhook/assess-product"
    payload = {
        "product_name": product,
        "company_name": company,
        "sha1": sha1,
    }
    final_payload = {"product": payload}
    response = send_post_request(url, payload)

    #TODO: Process this response to get the calculable value for scoring
    data = response.get("response_json")
    con = data["confidence"]
    #print(con)
    #print("\n---\n")
    score = 1.0 if con == "high" else 0.7 if con == "medium" else 0.4
    data["trust_score"] = score
    data["confidence_score"] = score
    #print(response)
    # Return only the JSON payload, or None if request failed
    return response.get("response_json") if response.get("success") else None

def call_webhook_security_assessment(product=None, company=None, url_param=None):
    """
    Sends a POST request with JSON content containing
    three parameters. Supports missing/None values.
    """
    print("call_webhook_security_assessment ...\n")
    url = "https://plantbase.app.n8n.cloud/webhook/6c08ca4a-e308-4b02-9c0e-2401a333e2c5"
    payload = {
        "product_name": product,
        "website": url_param,
    }
    final_payload = payload
    response = send_post_request(url, final_payload)

    if response.get("response_json") == None:
        return call_webhook_security_assessment(product, company, url_param)

    data = response.get("response_json")
    binary = data["security"]["binary"]
    # if binary is 0 then do not include
    data["trust_score"] = 0 if binary == 0  else 1
    data["trust_flag"] = False if binary == 0 else True
    data["confidence_score"] = 0 if binary == 0  else 1
    #TODO: Process this response to get the calculable value for scoring
    return response.get("response_json") if response.get("success") else None

    # Return only the JSON payload, or None if request failed
    # return response.get("response_json") if response.get("success") else None

def call_webhook_license_scan(product=None, company=None, url_param=None):
    """
    Sends a POST request with JSON content containing
    three parameters. Supports missing/None values.
    """
    print("call_webhook_license_scan ...\n")
    url = "https://plantbase.app.n8n.cloud/webhook/github-license-finder"
    payload = {
        "product_name": product,
        "company_name": company,
        "website": url_param,
    }
    final_payload = {"product": payload}
    response = send_post_request(url, final_payload)

    #TODO: Process this response to get the calculable value for scoring
    data = response.get("response_json")
    con = data["confidence"]
    #print(con)
    #print("\n---\n")
    score = 1.0 if con == "high" else 0.7 if con == "medium" else 0.4
    data["trust_score"] = score
    data["confidence_score"] = score
    # Return only the JSON payload, or None if request failed
    return response.get("response_json") if response.get("success") else None

def call_webhook_virustotal(product=None, company=None, sha1=None):
    """
    Sends a POST request with JSON content containing
    three parameters. Supports missing/None values.
    """
    print("call_webhook_virustotal ...\n")
    url = "https://plantbase.app.n8n.cloud/webhook/virustotal-check"
    payload = {
        "product_name": product,
        "company_name": company,
        "hash": sha1
    }
    final_payload = payload
    response = send_post_request(url, final_payload)
    if response.get("response_json") == None:
        return call_webhook_virustotal(product=None, company=None, sha1=None)
    #TODO: Process this response to get the calculable value for scoring
    data = response.get("response_json")
    # if benign = 1 then we trust that hash matches the product
    # if bening = 0 then indecisive
    # if benign = -1 then we don't know
    benign = data["ai_output"]["benign"]

    malicious = data["last_analysis_stats"]["malicious"]
    tscore = 0 if malicious > 0 else 1
    cscore = 0.5 if benign == 0 else 1 if benign ==1 else 0
    data["trust_score"] = (tscore + cscore)/2
    data["confidence_score"] = cscore
    # Return only the JSON payload, or None if request failed
    return response.get("response_json") if response.get("success") else None

def call_webhook_certs_scan(product=None, company=None, url_param=None):
    """
    Sends a POST request with JSON content containing
    three parameters. Supports missing/None values.
    """
    print("call_webhook_certs_scan ...\n")
    url = "https://plantbase.app.n8n.cloud/webhook/8c532972-bfd6-40dc-9ff2-9cb0dab6d135"
    payload = {
        "product_name": product,
        "website": url_param,
    }
    final_payload =  payload
    response = send_post_request(url, final_payload)

    if response.get("response_json") == None:
        return call_webhook_certs_scan(product, company, url_param)

    #TODO: Process this response to get the calculable value for scoring
    data=response.get("response_json")
    security_data = data["security"]
    if not security_data == None:
        #print(security_data)
        # Check if there are any elements except 'others' with binary '1'
        found_other_binary_1 = False
        others_binary_1 = False
        
        for key, value in security_data.items():
            if key == 'others':
                # Check if others has binary '1'
                if value.get('binary') == '1':
                    others_binary_1 = True
            else:
                # Check if any other security element has binary '1'
                if value.get('binary') == '1':
                    found_other_binary_1 = True
        
        # Apply scoring rules
        if found_other_binary_1:
            score = 1
        elif others_binary_1 and not found_other_binary_1:
            score = 0.5
        else:
            score = 0
        
        data["trust_score"] = score
        data["confidence_score"] = 0 if not security_data else 1
    else:
            print("Problem call_webhook_certs_scan ...\n")
    # Return only the JSON payload, or None if request failed
    return response.get("response_json") if response.get("success") else None

def send_post_request(url, payload):
    """
    Sends a POST request with JSON content containing
    three parameters. Supports missing/None values.
    """
    headers = {
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(url, json=payload, headers=headers)

        # Raise exception if status is not 200-level
        response.raise_for_status()

        return {
            "success": True,
            "status_code": response.status_code,
            "response_json": response.json() if response.content else None
        }

    except requests.exceptions.RequestException as e:
        return {
            "success": False,
            "error": str(e)
        }

def get_cve_data_summary(product=None):
    """Call the CVE function and then transform the trust score"""
    print("get_cve_data_summary ...\n")
    result_json = cve.get_cve_records_by_keyword(product_name=product,use_exact_match=False)
    return result_json

def calculate_average_trust_score(scores_dict):
    """
    Calculate average of trust scores including security_assessment_trust_score 
    only if it is an integer.
    
    Args:
        scores_dict: Dictionary containing the trust scores
    
    Returns:
        float: Average of the valid scores
    """
    
    # List of score keys to consider (excluding security_assessment_trust_score for now)
    base_keys = [
        'assess_product_trust_score', 
        'license_scan_trust_score', 
        'virustotal_trust_score', 
        'certs_scan_trust_score', 
        'cve_trust_score'
    ]
    
    valid_scores = []
    
    # Add base scores
    for key in base_keys:
        if key in scores_dict and isinstance(scores_dict[key], (int, float)):
            valid_scores.append(scores_dict[key])
    
    # Add security_assessment_trust_score only if it's an integer
    security_key = 'security_assessment_trust_score'
    if (security_key in scores_dict and 
        isinstance(scores_dict[security_key], int)):
        valid_scores.append(scores_dict[security_key])
    
    # Calculate average if we have valid scores
    if valid_scores:
        return sum(valid_scores) / len(valid_scores)
    else:
        return 0.0  

def decide(trust_score: float, confidence: str) -> str:
    if confidence == "low":
        return "Insufficient public evidence"

    if confidence == "medium":
        if trust_score < 0.35:
            return "Tool cannot be trusted (medium confidence)"
        elif trust_score > 0.75:
            return "Tool can be trusted (please check sources for more information)"
        else:
            return "Tool is probably safe but alternatives are suggested"

    # confidence == "high"
    if trust_score < 0.35:
        return "Tool cannot be trusted with high confidence"
    elif trust_score > 0.75:
        return "Tool can be trusted with high confidence"
    else:
        return "Tool is probably safe but alternatives are suggested"

def prepare_final_result(product=None, vendor=None, sha1=None):
    """
    Prepare the final result
    """
    response_assess_product = call_webhook_assess_product(product=product, company=vendor, sha1=sha1)

    url=response_assess_product["website"]
    hq_country=response_assess_product["hq_country"]
    github_repo=response_assess_product["github_repo"]
    summary_one_liner=response_assess_product["summary_one_liner"]
    assess_product_trust_score=response_assess_product["trust_score"]
    sources_assess_product=response_assess_product["sources"]
    assess_product_confidence_score=response_assess_product["confidence_score"]

    response_security_assessment = call_webhook_security_assessment(product=product, company=vendor, url_param=url)
    security_assessment_trust_score=response_security_assessment["trust_score"]
    security_assessment_trust_flag=response_security_assessment["trust_flag"]
    #sources_security_assessment=response_security_assessment["sources"]
    security_assessment_confidence_score=response_security_assessment["confidence_score"]

    response_license_scan = call_webhook_license_scan(product=product, company=vendor, url_param=url)
    license_scan_trust_score=response_license_scan["trust_score"]
    sources_license_scan=response_license_scan["sources"]
    license_scan_confidence_score=response_license_scan["confidence_score"]

    response_virustotal = call_webhook_virustotal(product=product, company=vendor, sha1=sha1)
    virustotal_trust_score=response_virustotal["trust_score"]
    #sources_virustotal=response_virustotal["sources"]
    virustotal_confidence_score=response_virustotal["confidence_score"]


    response_certs_scan = call_webhook_certs_scan(product=product, company=vendor, url_param=url)
    certs_scan_trust_score=response_certs_scan["trust_score"]
    #sources_certs_scan=response_certs_scan["sources"]
    certs_scan_confidence_score=response_certs_scan["confidence_score"]

    response_cve = get_cve_data_summary(product=product)
    cve_trust_score=response_cve["trust_score"]
    sources_cve="https://www.cve.org/"
    cve_confidence_score = 1
    
    trust_scores = {
        'assess_product_trust_score': assess_product_trust_score,
        'license_scan_trust_score': license_scan_trust_score,
        'virustotal_trust_score': virustotal_trust_score,
        'certs_scan_trust_score': certs_scan_trust_score,
        'cve_trust_score': cve_trust_score
    }
    if(security_assessment_trust_flag):
        trust_scores["security_assessment_trust_score"] = security_assessment_trust_score
    
    final_trust_score = calculate_average_trust_score(trust_scores)

    confidence_scores = {
        'assess_product_confidence_score': assess_product_confidence_score,
        'license_scan_confidence_score': license_scan_confidence_score,
        'virustotal_confidence_score': virustotal_confidence_score,
        'certs_scan_confidence_score': certs_scan_confidence_score,
        'cve_confidence_score': cve_confidence_score,
        'security_assessment_confidence_score': security_assessment_confidence_score
    }

    final_confidence_score = (assess_product_confidence_score + license_scan_confidence_score + 
                              virustotal_confidence_score + certs_scan_confidence_score+ 
                              cve_confidence_score + security_assessment_confidence_score)/6
    
    confidence = "LOW" if final_confidence_score < 4 else "MEDIUM" if final_confidence_score < 7 else "HIGH"

    sources = {
        'sources_assess_product': sources_assess_product,
        #'sources_security_assessment': sources_security_assessment,
        'sources_license_scan': sources_license_scan,
        #'sources_virustotal': sources_virustotal,
        #'sources_certs_scan': sources_certs_scan,
        'sources_cve': sources_cve
    }

    justification = decide(trust_score=final_trust_score, confidence=confidence)

    final_report = {
        "Product": product,
        "Company": vendor,
        "Hash": sha1,
        "hq_country": hq_country,
        "github_repo": github_repo,
        "confidence": confidence,
        "confidence_scores": confidence_scores,
        "summary_one_liner": summary_one_liner,
        "url": url,
        "Trustability": final_trust_score,
        "trust_scores": trust_scores,
        "Summary": justification,
        "Sources": sources
    }
    return final_report


#for testing only
# def main():
#     # product='1Password'
#     # company='1Password'
#     # sha1='e5ee385388b5fa57cc8374102d779d3c9849a57f'
#     # response = call_webhook_assess_product(product=product,company=company,sha1=sha1)
#     # print(response)
#     product="Zoom"
#     company="Zoom Video Communications, Inc."
#     sha1="fd797e4071afe131104c1d29cd0cb606da62f3d5"
#     url="https://www.zoom.com/"
#     # response=call_webhook_certs_scan(product=product,company=company,url_param=url)
#     response=call_webhook_security_assessment(product=product, company=company, url_param=url)
#     print(response)

# if __name__ == "__main__":
#     main()