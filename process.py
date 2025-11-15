import requests
import os
import graph
import cve

def call_webhook_assess_product(product=None, company=None, sha1=None):
    """
    Sends a POST request with JSON content containing
    three parameters. Supports missing/None values.
    """
    url = "https://plantbase.app.n8n.cloud/webhook/assess-product"
    payload = {
        "product_name": product,
        "company_name": company,
        "sha1": sha1,
    }
    final_payload = {"product": payload}
    response = send_post_request(url, payload)

    #TODO: Process this response to get the calculable value for scoring
    print(response)
    # Return only the JSON payload, or None if request failed
    return response.get("response_json") if response.get("success") else None

def call_webhook_security_assessment(product=None, company=None, url_param=None):
    """
    Sends a POST request with JSON content containing
    three parameters. Supports missing/None values.
    """
    url = "https://plantbase.app.n8n.cloud/webhook/security-assessment"
    payload = {
        "product_name": product,
        "website": url_param,
    }
    final_payload = {"product": payload}
    response = send_post_request(url, final_payload)

    #TODO: Process this response to get the calculable value for scoring
    return response
    # Return only the JSON payload, or None if request failed
    # return response.get("response_json") if response.get("success") else None

def call_webhook_license_scan(product=None, company=None, url_param=None):
    """
    Sends a POST request with JSON content containing
    three parameters. Supports missing/None values.
    """
    url = "https://plantbase.app.n8n.cloud/webhook/github-license-finder"
    payload = {
        "product_name": product,
        "company_name": company,
        "website": url_param,
    }
    final_payload = {"product": payload}
    response = send_post_request(url, final_payload)

    #TODO: Process this response to get the calculable value for scoring

    # Return only the JSON payload, or None if request failed
    return response.get("response_json") if response.get("success") else None

def call_webhook_virustotal(product=None, company=None, sha1=None):
    """
    Sends a POST request with JSON content containing
    three parameters. Supports missing/None values.
    """
    url = "https://plantbase.app.n8n.cloud/webhook/virustotal-check"
    payload = {
        "product_name": product,
        "company_name": company,
        "hash": sha1
    }
    final_payload = {"product": payload}
    response = send_post_request(url, final_payload)

    #TODO: Process this response to get the calculable value for scoring

    # Return only the JSON payload, or None if request failed
    return response.get("response_json") if response.get("success") else None

def call_webhook_certs_scan(product=None, company=None, url_param=None):
    """
    Sends a POST request with JSON content containing
    three parameters. Supports missing/None values.
    """
    url = "https://plantbase.app.n8n.cloud/webhook/8c532972-bfd6-40dc-9ff2-9cb0dab6d135"
    payload = {
        "product_name": product,
        "website": url_param,
    }
    final_payload = {"product": payload}
    response = send_post_request(url, final_payload)

    #TODO: Process this response to get the calculable value for scoring

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

def get_cve_data_summary(product=None, company=None, sha1=None):
    result_json = cve.get_cve_records_by_keyword(product_name=product,use_exact_match=False)
    return result_json

# --------------------------
# Placeholder Graph Generator
# --------------------------
def generate_graph(product):
    """
    Placeholder graph generation.
    Creates a dummy text file representing a graph.
    """
    output_path = graph.create_graph(product, 5,6,3,1)

    return output_path

def prepare_final_result(product=None, company=None, url_param=None):
    """
    Prepare the final result
    """
    trustability = 0
    justification = "Lorem Ipsum"
    graph_path="random/path"

    final_result = {
        "Product": product,
        "Company": company,
        "url": url_param,
        "Trustability": trustability,
        "Summary": justification,
        "Graph": graph_path
    }

    return final_result


# # for testing only
# def main():
#     # product='1Password'
#     # company='1Password'
#     # sha1='e5ee385388b5fa57cc8374102d779d3c9849a57f'
#     # response = call_webhook_assess_product(product=product,company=company,sha1=sha1)
#     # print(response)
#     product="Zoom"
#     company="Zoom Video Communications, Inc."
#     url="fd797e4071afe131104c1d29cd0cb606da62f3d5"
#     # response=call_webhook_license_scan(product=product,company=company,url_param=url)
#     response=get_cve_data_summary(product=product,company=company,sha1=url)
#     print(response)

# if __name__ == "__main__":
#     main()
