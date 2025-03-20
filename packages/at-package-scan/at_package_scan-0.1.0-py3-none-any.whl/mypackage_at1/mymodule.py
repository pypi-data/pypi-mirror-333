import subprocess
import json
import argparse


def scan(registry, tag_or_digest):
    """Scans a container image using Trivy and returns JSON results."""
    image = f"{registry}:{tag_or_digest}"
    print("Response from image scan using trivy , {image} and {tag}")


    try:
        result = subprocess.run(
            ["trivy", "image", "--format", "json", image],
            capture_output=True, text=True, check=True
        )
        
        # Parse JSON output
        vulnerabilities = json.loads(result.stdout)
        
        return vulnerabilities

    except subprocess.CalledProcessError as e:
        print("Error running Trivy:", e)
        return None
    except json.JSONDecodeError:
        print("Error parsing Trivy output")
        return None

