import os
import requests

try:
    from importlib.metadata import version
except ImportError:
    from importlib_metadata import version

from surge.projects import Project
from surge.tasks import Task
from surge.teams import Team
from surge.reports import Report
from surge.rubrics import Rubric

try:
    __version__ = version("surge-api")
except Exception:
    __version__ = "unknown"

api_key = os.environ.get("SURGE_API_KEY", None)
base_url = os.environ.get("SURGE_BASE_URL", "https://app.surgehq.ai/api")

session = requests.Session()
session.headers.update({"User-Agent": f"surge-python/{__version__}"})
