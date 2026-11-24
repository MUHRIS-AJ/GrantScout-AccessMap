import unittest
from unittest.mock import patch
import core
class Tests(unittest.TestCase):
    @patch("core.request_json")
    def test_grants(self,fetch):
        fetch.return_value={"errorcode":0,"data":{"oppHits":[{"id":123,"number":"A-01","title":"Research grant","agencyName":"Agency","oppStatus":"posted"}]}}
        r=core.run("research","GrantScout")
        self.assertEqual(r["count"],1)
        self.assertIn("grants.gov",r["opportunities"][0]["source_url"])
    @patch("core.request_json")
    def test_access(self,fetch):
        fetch.return_value={"elements":[{"id":321,"type":"node","lat":6,"lon":80,"tags":{"wheelchair":"yes","name":"Example"}}]}
        r=core.run("6,80","AccessMap")
        self.assertEqual(r["places"][0]["wheelchair_tag"],"yes")
        self.assertFalse(r["places"][0]["on_site_verified"])
    def test_coordinate_validation(self):
        with self.assertRaises(ValueError):core.accessibility("somewhere")
        with self.assertRaises(ValueError):core.accessibility("91,181")
if __name__=="__main__":unittest.main()
