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

def main():
    print("in main")
    parser = argparse.ArgumentParser(description="Scan a container image using Trivy")
    
    parser.add_argument("--registry", required=True, help="Container registry (e.g., docker.io/nginx)")
    parser.add_argument("--tag", required=True, help="Image tag or digest (e.g., latest or sha256:12345)")
    
    args = parser.parse_args()

    print(f"Scanning image: {args.registry}:{args.tag} ...")
    
    results = scan(args.registry, args.tag)

    if results:
        print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()