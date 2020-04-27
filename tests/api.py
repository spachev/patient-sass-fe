import unittest
import requests
import random
import json

TEST_URL_BASE="http://64.227.4.120:8001"

class APITester(unittest.TestCase):
  def send_json(self, path, json):
    return requests.post(TEST_URL_BASE + path, json=json)

  def send_get(self, path, params):
    return requests.get(TEST_URL_BASE + path + params)

  def test_result_category(self):
    random_identifier = str(random.randint(10**5,10**6-1)) #so we can rerun tests
    data = {"name" : "Test Patience"+random_identifier, "email" : "test"+random_identifier+"@test.com", "mobile_number": "1234567890",
        "postal_address" : "123 Test, Salt Lake City, UT", "tenant_id" : 1}
    req_o = data
    rsp = self.send_json("/patient/insert", req_o)
    self.assertTrue(rsp.status_code == 201, "Bad status response code: {}".format(rsp.status_code))
    rsp_o = rsp.json()
    print(rsp_o)
    id = rsp_o["id"]
    self.assertTrue(rsp_o["msg"] == 'Operation Successful', "Got unexpected msg in response {}".format(rsp_o["msg"]))
    rsp = self.send_json("/patient/insert", req_o)
    self.assertTrue(rsp.status_code == 409, "Bad status response code: {}".format(rsp.status_code))
    rsp = self.send_get("/patient", "/{}".format(id))
    self.assertTrue(rsp.status_code == 200, "Bad status response code: {}".format(rsp.status_code))
    rsp_o = rsp.json()
    expect_rsp_o = data.copy()
    expect_rsp_o["id"] = id
    expect_rsp_o["create_datetime"] = rsp_o["create_datetime"]
    self.assertTrue(rsp_o == expect_rsp_o, "Got unexpected data: {}, expected {}".format(rsp_o, expect_rsp_o))

    #updating a record
    data2 = {"mobile_number": "123224323", "id" : 1}
    rsp = self.send_json("/patient/update", data2)
    self.assertTrue(rsp.status_code == 201, "Bad status response code: {}".format(rsp.status_code))
    rsp_o = rsp.json()
    self.assertTrue(rsp_o["msg"] == 'Operation Successful', "Got unexpected msg in response {}".format(rsp_o["msg"]))

    #deleting a record
    data3 = {"id": id}
    rsp = self.send_json("/patient/delete", data3)
    self.assertTrue(rsp.status_code == 201, "Bad status response code: {}".format(rsp.status_code))
    rsp_o = rsp.json()
    id = rsp_o["id"]
    self.assertTrue(rsp_o["msg"] == 'Operation Successful', "Got unexpected msg in response {}".format(rsp_o["msg"]))
if __name__ == '__main__':
  unittest.main()
