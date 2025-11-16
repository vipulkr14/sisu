#!/usr/bin/env python3
#!/usr/bin/env python3
import click
import os
import random
import process
from datetime import date, datetime, timedelta
import cache
import graph
import report

def is_expired(expiry_date):
    now_naive = datetime.now()  # Current time (naive)
    
    # If expiry_date is aware, make it naive
    if expiry_date.tzinfo is not None:
        expiry_date = expiry_date.replace(tzinfo=None)
    
    return expiry_date < now_naive

def process_inputs(product, vendor, sha1):
    """
    Determines which parameters were provided
    and returns a structured message + dummy trust score.
    """
    #Check cache first
    # if not in cache then calculate everything and update cache
    product_manager = cache.ProductManager()
    fetched_data = product_manager.get_product_by_name(product_name=product)
    if fetched_data is None:
        print("Fetching data ...\n")
        final_result = process.prepare_final_result(product=product, vendor=vendor, sha1=sha1)
        product_manager.create_product(product=product, product_data=final_result)
        fetched_data = final_result
    else:
        #If expired then calculate again and create in cache
        expiry_date = fetched_data["expiry_date"]
        if is_expired(expiry_date=expiry_date):
            print("Expired data!\n")
            print("Fetching data ...\n")
            id=fetched_data["id"]
            final_result = process.prepare_final_result(product=product, vendor=vendor, sha1=sha1)
            product_manager.update_full_product(product_id=id, product_data=final_result)
            fetched_data = final_result
    
    return fetched_data


def generate_graph(product, trust_scores):
    """
    Placeholder graph generation.
    Creates a dummy text file representing a graph.
    """
    output_path = graph.create_graph(product=product, trust_scores=trust_scores)

    return output_path


# --------------------------
# CLI Definition
# --------------------------
@click.command()
@click.option("--product", type=str, required=False, help="Product Name.")
@click.option("--vendor", type=str, required=False, help="Vendor/Company Name")
@click.option("--sha1", type=str, required=False, help="SHA1")
def cli(product, vendor, sha1):
    """
    A single CLI that accepts up to four parameters,
    processes them, and generates a trust score + a graph.
    """

    click.echo("Processing inputs...")

    # Placeholder processing
    final_result = process_inputs(product, vendor, sha1)

    # Generate placeholder graph
    graph_path = generate_graph(product, final_result["trust_scores"])

    #generate report
    report_path = report.generate_report(product=product, data=final_result, graph_path=graph_path)
    # Final output
    click.echo(f"📊 The report can be found at: {report_path}\n")


# Entry point
if __name__ == "__main__":
    cli()


###
## Given minimal input (product name, vendor, or URL), build a system that:

## Resolves the entity and vendor identity.
## Classifies the software into a clear taxonomy (e.g., File sharing, GenAI tool, SaaS CRM, Endpoint agent).
## Produces a concise security posture summary with citations.
## Covers: description, usage, vendor reputation, CVE trend summaries (Common Vulnerabilities and Exposures), incidents/abuse signals, data handling/compliance, deployment/admin controls, and transparent 0–100 trust/risk score with rationale and confidence.
## Suggests 1–2 safer alternatives with short rationale.
## 

## Insight
## Focus on high-signal sources: vendor security/PSIRT pages (Product Security Incident Response Team),
# Terms of Service/Data Processing Agreement, (System and Organization Controls Type II),
#  ISO attestations, reputable advisories/CERTs (Notices from Computer Emergency Response Teams or vendors),
#  and CISA KEV (CISA Known Exploited Vulnerabilities catalog). 
# Guard against hallucinations by labeling vendor-stated vs. independent claims. 
# When data is scarce, return “Insufficient public evidence.”