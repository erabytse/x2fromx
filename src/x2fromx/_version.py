"""Version helper with fallback for development installs."""
from importlib.metadata import version, PackageNotFoundError

def get_version() -> str:
    try:
        return version("x2fromx")
    except PackageNotFoundError:
        # Fallback pour 'pip install -e .' en dev
        return "0.1.3-dev"