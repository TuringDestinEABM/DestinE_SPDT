from digitalTwin.library import getData

def test_loadJSONdata(dummy_metadata_1, tmp_geodata):
      filepath = tmp_geodata / "example1/metadata.json"
      data = getData.loadJSONdata(filepath)
      assert data == dummy_metadata_1

# def test_listAvailableReports():
#       data = getData.listAvailableReports(path)