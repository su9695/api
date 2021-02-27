import pytest
import requests

@pytest.fixture(scope='module')
def oSession():
    ompsession = requests.session()
    obpsession = requests.session()
    ospsession = requests.session()
    s = {}
    s['ompsession'] = ompsession
    s['obpsession'] = obpsession
    s['ospsession'] = ospsession
    yield s

@pytest.fixture
def getParam(request):
    return request.param


    
