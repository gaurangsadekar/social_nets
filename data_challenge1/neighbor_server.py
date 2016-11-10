from __future__ import print_function
import requests

def get_url_and_uni(opt):
    SERVER_URL = "https://6io70nu9pi.execute-api.us-east-1.amazonaws.com/smallworld/"
    TEST_URL = "https://6io70nu9pi.execute-api.us-east-1.amazonaws.com/datachallenge/"
    TRAIN_UNI = "gss2147"
    TEST_UNI = "lambda"
    if opt == "test":
        return TEST_URL, TEST_UNI
    else:
        return SERVER_URL, TRAIN_UNI

def get_testcase(testcase_id, opt):
    try:
        url, _ = get_url_and_uni(opt)
        start_test_url = url + "start/" + str(testcase_id)
        resp = requests.get(start_test_url)
        testcase = resp.json()
        assert(int(testcase["reach testcase number"]) == testcase_id)
        return (int(testcase["source node"]), int(testcase["target node"]))
    except AssertionError:
        print("Testcase requested wasn't the one returned")

# get neighbors from API and adjust datatypes
def get_neighbors(node_id, testcase_id, opt):
    url, uni = get_url_and_uni(opt)
    neighbor_url = url + "neighbors?node=" + str(node_id) + "&uni=" + uni + "&testcaseID=" + str(testcase_id)
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

# will submit only for test URL,
# use carefully, graded pretty stringently
def submit_path_for_testcase(testcase_id, path_list):
    url, uni = get_url_and_uni("test")
    path_str = "path=" + ",".join(map(lambda x: str(x), path_list))
    submission_url = url + "submit?testcaseID=" + str(testcase_id) + "&" + path_str + "&uni=" + uni
    try:
        submission_resp = requests.post(submission_url)
        assert(submission_resp.status_code == 200)
        print("Submitted test case:", testcase_id)
        print(submission_resp.json())
    except AssertionError:
        print("Submission Error: May have already submitted path for this test case")
    try:
        check_sub_url = url + "check/" + uni + "/" + str(testcase_id)
        check_resp = requests.get(check_sub_url)
        assert(check_resp.status_code == 200)
        print(check_resp.json())
    except AssertionError:
        print("Submission Check didn't work")

if __name__ == "__main__":
    submit_path_for_testcase(1, [1,2,3,4])
