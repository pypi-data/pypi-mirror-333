import json
import subprocess

class TrivyScanner:
    def __init__(self):
        """Initialize a scanner that runs Trivy in Docker."""
        pass

    def scan(self, registry, tag_or_digest):
        """Scans an image using Trivy inside a Docker container."""
        image = f"{registry}:{tag_or_digest}"
        print(f"Scanning image: {image} using Dockerized Trivy")

        try:
            result = subprocess.run(
                [
                    "docker", "run", "--rm",
                    "-v", "/var/run/docker.sock:/var/run/docker.sock",
                    "aquasec/trivy", "image", "--format", "json", image
                ],
                capture_output=True, text=True, check=True
            )
            return json.loads(result.stdout)
        except subprocess.CalledProcessError as e:
            print("Error running Trivy in Docker:", e)
            return None
        except json.JSONDecodeError:
            print("Error parsing Trivy output")
            return None