import json
import urllib.parse
import requests
import os
from .mock_requests import get, getName, MockResponse

"""
Rebuild distribution files:
rm -rf dist/
python setup.py sdist bdist_wheel

Re-upload to PyPI:
twine upload dist/*

To install locally:
pip install dist/mock_requests-1.9.0-py3-none-any.whl --force-reinstall

Helpful video:
https://www.youtube.com/watch?v=Kz6IlDCyOUY
"""

