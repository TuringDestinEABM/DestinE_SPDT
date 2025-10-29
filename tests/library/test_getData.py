from digitalTwin.library import getData
import pytest

"""Tests for test_loadJSONdata"""
def test_loadJSONdata_11(dummy_metadata_1, tmp_geodata):
      "Check that example1/metadata loads is the same as dummy_metadata_1"
      filepath = tmp_geodata / "results/example1/metadata.json"
      data = getData.loadJSONdata(filepath)
      assert data["id"] == dummy_metadata_1["id"]
      assert data["name"] == dummy_metadata_1["name"]
      assert data["Days"] == dummy_metadata_1["Days"]

def test_loadJSONdata_22(dummy_metadata_2, tmp_geodata):
      "Check that example2/metadata loads in the same as dummy_metadata_1"
      filepath = tmp_geodata / "results/example2/metadata.json"
      data = getData.loadJSONdata(filepath)
      assert data["id"] == dummy_metadata_2["id"]
      assert data["name"] == dummy_metadata_2["name"]
      assert data["Days"] == dummy_metadata_2["Days"]

def test_loadJSONdata_21(dummy_metadata_1, tmp_geodata):
      "Check that example2/metadata loads in different to dummy_metadata_1"
      filepath = tmp_geodata / "results/example2/metadata.json"
      data = getData.loadJSONdata(filepath)
      assert not (data["id"]== dummy_metadata_1["id"])

def test_loadJSONdata_12(dummy_metadata_2, tmp_geodata):
      "Check that example2/metadata loads in different to dummy_metadata_1"
      filepath = tmp_geodata / "results/example1/metadata.json"
      data = getData.loadJSONdata(filepath)
      assert not (data["id"]== dummy_metadata_2["id"])

"""tests for listAvailableReports"""

"""tests for findGEOData"""

"""tests for findMetadata"""

"""tests for listSummaryFigures"""

"""tests for listAvailableReports"""
# @pytest.mark.dependency(scope='session')
def test_listAvailableReports(tmp_geodata, dummy_metadata_1, dummy_metadata_2):
      file_path = tmp_geodata / "results"
      data = getData.listAvailableReports(file_path)
      row0 =  data.get("files")[0]
      row1 =  data.get("files")[1]

      assert len(data) == 1
      assert row0.get("name")== dummy_metadata_1["name"]
      assert row1.get("id") == dummy_metadata_2["id"]