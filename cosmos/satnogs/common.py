import os
BASE_URL = 'https://db.satnogs.org'
API_TOKEN = os.getenv('SATNOGS_API_TOKEN')
CACHE_DIR = 'cache/'
STRUCT_DIR = 'ksy/'
KNOWN_IDS_PATH = CACHE_DIR + 'known-satellites.json'
TEMPLATE_SATELITE = CACHE_DIR + 'NID-satellite.json'
TEMPLATE_TELEMETRY = CACHE_DIR + 'NID-telemetry.json'
TEMPLATE_STRUCTURE = STRUCT_DIR + 'NID-structure.ksy'
