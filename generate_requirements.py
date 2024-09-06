import os
import pkg_resources
import subprocess

def get_installed_packages():
    """Get a list of installed packages and their versions."""
    return [f"{dist.project_name}=={dist.version}" for dist in pkg_resources.working_set]

def get_imported_modules():
    """Get a list of imported modules in the project."""
    command = 'grep -r "^import " . | grep -v "venv" | cut -d " " -f 2 | sort | uniq'
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return result.stdout.splitlines()

def generate_requirements():
    """Generate the requirements.txt file."""
    installed_packages = get_installed_packages()
    imported_modules = get_imported_modules()

    # Filter installed packages to only those that are imported
    required_packages = [pkg for pkg in installed_packages if any(pkg.startswith(module) for module in imported_modules)]

    # Add Flask, CrewAI and other essential packages
    essential_packages = [
        "flask",
        "crewai",
        "psycopg2-binary",
        "elasticsearch",
        "milvus-python-sdk",
        "spacy",
        "nltk",
        "asyncio",
        "aiohttp",
        "python-jose[cryptography]",
        "passlib[bcrypt]",
        "prometheus-client",
        "pika",
        "kafka-python",
        "openai",
        "anthropic",
        "google-generativeai",
        "azure-openai",
        "python-dotenv",
        "requests",
        "pydantic"
    ]

    for package in essential_packages:
        if not any(pkg.startswith(package) for pkg in required_packages):
            required_packages.append(package)

    # Write the requirements to a file
    with open("requirements.txt", "w") as f:
        for package in sorted(required_packages):
            f.write(f"{package}\n")

    print("requirements.txt file has been generated.")

if __name__ == "__main__":
    generate_requirements()