import pytest

"""Test 404"""
def test_nonexistent_route(client):
    response = client.get('/ThisROuteDoesNoTeXist')
    assert response.status_code == 404

# class TestStatusCodes:
"""Test that requests are returning valid pages"""
def test_status_code_home(client):
    response = client.get('/')
    assert response.status_code == 302

def test_status_code_home(client):
    response = client.get('/home')
    assert response.status_code == 200

def test_status_code_contact(client):
    response = client.get('/contact')
    assert response.status_code == 200

def test_status_code_createscenario(client):
    response = client.get('/createscenario')
    assert response.status_code == 200

def test_status_code_data_sources(client):
    response = client.get('/data_sources')
    assert response.status_code == 200

def test_status_code_help(client):
    response = client.get('/help')
    assert response.status_code == 200

def test_status_code_queue(client):
    response = client.get('/queue')
    assert response.status_code == 200

def test_status_code_report(client):
    response = client.get('/reports')
    assert response.status_code == 200

"""Test redirects"""
def test_redirect_slash(client):
    response = client.get('/', follow_redirects=True)
    assert len(response.history) == 1
    assert response.request.path == "/home"

# # """Test routes with GET requests"""
# @pytest.mark.dependency(depends=["library/test_getData.py::test_listAvailableReports"]) #dependency doesnt seem to work session scope
# def test_GET_reports(client):
#     response = client.get('/reports')
#     assert len(response.data) == 1

# def test_status_code_report_ID(client):
#     validResponse = client.get('/report/validID')
#     invalidResponse = client.get('/report/invalidID')
#     assert validResponse.status_code == 200
#     assert invalidResponse.status_code == 400

# def test_status_code_report_ID_timeline(client):
#     validResponse = client.get('/report/validID/timeline')
#     invalidResponse = client.get('/report/invalidID/timeline')
#     assert validResponse.status_code == 200
#     assert invalidResponse.status_code == 400

# def test_status_code_settings(client):
#     response = client.get('/settings')
#     assert response.status_code == 200

# class TestGETRequests:
#     """Test that routes which GET data for the user are doing so correctly.
#     These tests should depend on the tests for the corresponding getdata.py scripts or equivalent"""

# class TestPOSTRequests:
#     """Test that routes which POST data from the user are doing so correctly.
#     These tests should depend on the tests for the corresponding forms.py scripts or equivalent"""