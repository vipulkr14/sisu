import requests
import os
import graph

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

    response = send_post_request(url, payload)

    #TODO: Process this response to get the calculable value for scoring

    return response

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

    response = send_post_request(url, payload)

    #TODO: Process this response to get the calculable value for scoring

    return response

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

    return response

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


def main():
    # product='1Password'
    # company='1Password'
    # sha1='e5ee385388b5fa57cc8374102d779d3c9849a57f'
    # response = call_webhook_assess_product(product=product,company=company,sha1=sha1)
    # print(response)
    product="PeaZip"
    company="Giorgio Tani"
    url="https://github.com/peazip/PeaZip"
    response=call_webhook_license_scan(product=product,company=company,url_param=url)
    print(response)

if __name__ == "__main__":
    main()
