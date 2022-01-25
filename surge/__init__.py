import os

from surge.projects import Project
from surge.tasks import Task
from surge.reports import Report

api_key = os.environ.get("SURGE_API_KEY", None)
