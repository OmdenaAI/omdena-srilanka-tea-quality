from .test import TestsApi
from .inference import InferencesApi


def initialize_routes(api):
    api.add_resource(TestsApi, '/api/tests')
    api.add_resource(InferencesApi, '/api/inferences')
