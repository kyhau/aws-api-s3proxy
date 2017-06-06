"""
Test Data Service (API Gateway) Methods
"""
import datetime
import json
from time import mktime

# HTTP Status Codes considered as OK
HTTPS_OK_CODES = [200, 201]
HTTPS_NOT_OK_CODES = [400]


class DefaultEncoder(json.JSONEncoder):
    """Encode for the json
    """
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return int(mktime(obj.timetuple()))
        return json.JSONEncoder.default(self, obj)


def test_data_service(apig_client, aws_settings, sample_test_file):
    """Test Data Service resources.
    """
    apig_id = aws_settings['aws_restapiid']
    bucket = aws_settings['aws_s3']

    # Retrieve info of all resources
    resp = apig_client.get_resources(restApiId=apig_id, limit=25)
    ret = resp['ResponseMetadata']['HTTPStatusCode'] in HTTPS_OK_CODES
    if ret is False:
        print('Response:\n{}'.format(json.dumps(resp, cls=DefaultEncoder, indent=2)))
    assert ret

    ###########################################################################
    # Expected 1 resource: `item` and 2 items including '/'
    expected_items = {
        '/':'',
        '/item':''
    }
    assert len(resp['items']) == len(expected_items.items())

    for item in resp['items']:
        assert item['path'] in expected_items.keys()
        expected_items[item['path']] = item['id']

    ###########################################################################
    # Test each resource and its methods

    with open(sample_test_file, 'r') as fp:
        new_data = fp.read()

    basepath = '/item?key={}'.format(bucket)

    test_cases = [
        # HEAD - Fail: invalid bucket
        {'path':'/item', 'method':'HEAD', 'querystr':'/item', 'body':'', 'pass':False},

        # HEAD - Pass: valid bucket
        {'path':'/item', 'method':'HEAD', 'querystr':basepath, 'body':'', 'pass':True},

        # HEAD - Fail: invalid bucket
        {'path':'/item', 'method':'HEAD', 'querystr':'/item?key=nonexistbucket', 'body':'', 'pass':False},

        # PUT - Pass: add new bucket/file
        {'path':'/item', 'method':'PUT', 'querystr':'{}/{}'.format(basepath,'data_service_pytest_1.json'), 'body':new_data, 'pass':True},
        # GET - Pass: confirm file added
        {'path':'/item', 'method':'GET', 'querystr':'{}/{}'.format(basepath,'data_service_pytest_1.json'), 'body':'', 'pass':True},

        # PUT - Pass: add new bucket/folder/folder/file
        {'path': '/item', 'method': 'PUT', 'querystr': '{}/a/b/{}'.format(basepath, 'data_service_pytest_2.json'), 'body':new_data, 'pass':True},
        # GET - Pass: confirm file added
        {'path': '/item', 'method': 'GET', 'querystr': '{}/a/b/{}'.format(basepath, 'data_service_pytest_2.json'),'body':'', 'pass':True},

        # PUT - Pass: overwrite bucket/file
        {'path': '/item', 'method': 'PUT', 'querystr': '{}/{}'.format(basepath, 'data_service_pytest_1.json'), 'body':'helloworld', 'pass':True},

        # DELETE - Pass: delete bucket/file
        {'path': '/item', 'method': 'DELETE', 'querystr': '{}/{}'.format(basepath, 'data_service_pytest_1.json'), 'body':'', 'pass':True},
        # GET - Pass: confirm file deleted
        {'path': '/item', 'method': 'GET', 'querystr': '{}/a/b/{}'.format(basepath, 'data_service_pytest_2.json'),'body':'', 'pass':False},

        # DELETE - Pass: delete bucket/folder/folder/file
        {'path': '/item', 'method': 'DELETE', 'querystr': '{}/a/b/{}'.format(basepath, 'data_service_pytest_2.json'), 'body':'', 'pass':True},
        # GET - Pass: confirm file deleted
        {'path': '/item', 'method': 'GET', 'querystr': '{}/a/b/{}'.format(basepath, 'data_service_pytest_2.json'),'body':'', 'pass':False},

    ]

    # NOTES: Need an empty headers
    #   Known issue: Internal Server Error Only When Testing Invoke Method via AWS API
    #   https://forums.aws.amazon.com/thread.jspa?threadID=248714&tstart=0
    for test_case in test_cases:
        print("Testing {} {}".format(test_case['method'], test_case['querystr']))
        resp = apig_client.test_invoke_method(
            restApiId=apig_id,
            resourceId=expected_items[test_case['path']],
            httpMethod=test_case['method'],
            pathWithQueryString=test_case['querystr'],
            headers={},
            body=test_case['body']
        )
        ret = resp['status'] in HTTPS_OK_CODES if test_case['pass'] else HTTPS_NOT_OK_CODES
        if ret is False:
            print('Response:\n{}'.format(json.dumps(resp, cls=DefaultEncoder, indent=2)))
        assert ret
