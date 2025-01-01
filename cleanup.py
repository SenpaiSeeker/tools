import sys
import requests

PYPI_API_BASE_URL = "https://pypi.org"

def get_headers(token):
    return {"Authorization": f"Bearer {token}"}

def get_package_versions(package_name, token):
    url = f"{PYPI_API_BASE_URL}/pypi/{package_name}/json"
    response = requests.get(url, headers=get_headers(token))
    if response.status_code != 200:
        print(f"Failed to fetch package versions. HTTP {response.status_code}: {response.text}")
        sys.exit(1)
    data = response.json()
    return list(data.get('releases', {}).keys())

def delete_version(package_name, version, token):
    url = f"{PYPI_API_BASE_URL}/manage/project/{package_name}/release/{version}/"
    response = requests.delete(url, headers=get_headers(token))
    if response.status_code != 204:
        print(f"Failed to delete version {version}. HTTP {response.status_code}: {response.text}")
        return False
    return True

def main():
    if len(sys.argv) != 3:
        print("Usage: python cleanup.py <pypi_token> <package_name>")
        sys.exit(1)

    pypi_token, package_name = sys.argv[1], sys.argv[2]

    print(f"Fetching versions for package {package_name}...")
    versions = get_package_versions(package_name, pypi_token)

    if not versions:
        print(f"No versions found for package {package_name}.")
        sys.exit(0)

    print(f"Found versions: {', '.join(versions)}")

    for version in versions:
        print(f"Deleting version {version}...")
        if delete_version(package_name, version, pypi_token):
            print(f"Successfully deleted version {version}.")
        else:
            print(f"Failed to delete version {version}. Exiting...")
            sys.exit(1)

    print(f"All versions of {package_name} have been deleted successfully.")

if __name__ == "__main__":
    main()
