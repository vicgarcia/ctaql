"""
bustracker

contains functionality for ...
- client library for accessing the CTA bustracker API
- cli command to parse/sync data from bustracker API to local DB
"""

from django.apps import AppConfig

class BustrackerConfig(AppConfig):
    name = 'bustracker'
