from __future__ import print_function
import requests

SERVER_URL = "https://6io70nu9pi.execute-api.us-east-1.amazonaws.com/smallworld/"
UNI= "gss2147"

def get_testcase(testcase_id):
    try:
        start_test_url = SERVER_URL + "start/" + str(testcase_id)
        resp = requests.get(start_test_url)
        testcase = resp.json()
        assert(int(testcase["reach testcase number"]) == testcase_id)
        return (int(testcase["source node"]), int(testcase["target node"]))
    except AssertionError:
        print("Testcase requested wasn't the one returned")

# get neighbors from API and adjust datatypes
def get_neighbors(node_id, testcase_id):
    neighbor_url = SERVER_URL + "neighbors?node=" + str(node_id) + "&uni=" + UNI + "&testcaseID=" + str(testcase_id)
    resp = requests.get(neighbor_url)
    resp_json = resp.json()
    neighbors_list = resp_json["neighbors"]
    result_neighbors = {}
    for neighbor in neighbors_list:
        for node, props in neighbor.iteritems():
            prop_dict = {}
            prop_dict["deg"] = props[0]
            prop_dict["local_clu"] = props[1]
            result_neighbors[int(node)] = prop_dict
    return result_neighbors

def submit_path_for_testcase(testcase_id, path_list):
    path_str = "path=" + ",".join(map(lambda x: str(x), path_list))
    submission_url = SERVER_URL + "submit?testcaseID=" + str(testcase_id) + "&" + path_str + "&uni=" + UNI
    try:
        submission_resp = requests.post(submission_url)
        assert(submission_resp.status_code == 200)
        print("Submitted test case:", testcase_id)
        print(submission_resp.json())
    except AssertionError:
        print("Submission Error: May have already submitted path for this test case")
    try:
        check_sub_url = SERVER_URL + "check/" + UNI + "/" + str(testcase_id)
        check_resp = requests.get(check_sub_url)
        assert(check_resp.status_code == 200)
        print(check_resp.json())
    except AssertionError:
        print("Submission Check didn't work")

if __name__ == "__main__":
    submit_path_for_testcase(1, [1,2,3,4])
