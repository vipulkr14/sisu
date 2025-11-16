import base64
from jinja2 import Environment, FileSystemLoader
import json


data = {
    # paste your dict here if needed; otherwise load dynamically
}


def encode_image_to_base64(path):
    with open(path, "rb") as img:
        return base64.b64encode(img.read()).decode("utf-8")


def generate_report(product, data, graph_path):
    # load Jinja2 template
    env = Environment(loader=FileSystemLoader("templates"))
    template = env.get_template("report.html")

    # encode graph image
    data["graph_b64"] = encode_image_to_base64(graph_path)

    # render HTML
    html = template.render(**data)

    # write output
    report_path = "output/"+product+"_report.html"
    with open(report_path, "w") as f:
        f.write(html)

    #print("✓ Report generated: output/final_report.html")
    return report_path


# if __name__ == "__main__":
#     generate_report(data)
