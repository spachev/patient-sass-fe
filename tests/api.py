import unittest
import requests
import json

TEST_URL_BASE="http://localhost:8001"

class APITester(unittest.TestCase):
  def send_json(self, path, json):
    return requests.post(TEST_URL_BASE + path, json=json)

  def send_get(self, path, params):
    return requests.get(TEST_URL_BASE + path + params)

  def test_result_category(self):
    data = {"name" : "Test Patience", "email" : "test@test.com", "mobile_number": "1234567890",
        "postal_address" : "123 Test, Salt Lake City, UT", "tenant_id" : 1}
    req_o = data
    rsp = self.send_json("/patient/insert", req_o)
    self.assertTrue(rsp.status_code == 201, "Bad status response code: {}".format(rsp.status_code))
    rsp_o = rsp.json()
    id = rsp_o["id"]
    self.assertTrue(id == 1, "Got unrespected ID in response {}".format(rsp_o["id"]))
    rsp = self.send_json("/patient/insert", req_o)
    self.assertTrue(rsp.status_code == 409, "Bad status response code: {}".format(rsp.status_code))
    rsp = self.send_get("/patient", "/{}".format(id))
    self.assertTrue(rsp.status_code == 200, "Bad status response code: {}".format(rsp.status_code))
    rsp_o = rsp.json()
    expect_rsp_o = data.copy()
    expect_rsp_o["id"] = id
    expect_rsp_o["create_datetime"] = rsp_o["create_datetime"]
    self.assertTrue(rsp_o == expect_rsp_o, "Got unexpected data: {}, expected {}".format(rsp_o, expect_rsp_o))
if __name__ == '__main__':
  unittest.main()
