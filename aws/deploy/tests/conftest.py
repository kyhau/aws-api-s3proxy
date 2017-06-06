"""
conftest.py
"""
import boto3
import configparser
import json
import os
import py.test
from os.path import dirname, exists, join, realpath
from shutil import rmtree
from tempfile import mkdtemp


###############################################################################
# py.test options and env variables

ENV_AWS_ACCESS_KEY_ID = 'aws_access_key_id'
ENV_AWS_SECRET_ACCESS_KEY = 'aws_secret_access_key'

SETTINGS = {
    'api_json_file': join(dirname(dirname(dirname(dirname(realpath(__file__))))), 'api', 'DataServiceAPI_swagger.json'),
    'aws_region': 'ap-southeast-2',
    'ini_file': join(dirname(dirname(realpath(__file__))), 'aws.ini'),
}

###############################################################################
# py.test fixtures

@py.test.fixture(scope='module')
def config():
    config = configparser.ConfigParser()
    config.read(SETTINGS['ini_file'])
    return config


@py.test.fixture(scope='module')
def aws_settings(config):
    """Retrieve AWS resource settings from the ini file.
    """
    settings = SETTINGS
    settings['aws_restapiid'] = config['default']['aws.apigateway.restApiId']
    settings['aws_access_key_id'] = os.environ[ENV_AWS_ACCESS_KEY_ID]
    settings['aws_secret_access_key'] = os.environ[ENV_AWS_SECRET_ACCESS_KEY]
    settings['aws_s3'] = config['test']['aws.s3']
    return settings


@py.test.fixture(scope='module')
def apig_client(aws_settings):
    return boto3.client(
        'apigateway',
        aws_access_key_id=aws_settings['aws_access_key_id'],
        aws_secret_access_key=aws_settings['aws_secret_access_key'],
        region_name=aws_settings['aws_region']
    )


def stage_settings(config, stage_name, settings):
    """Retrieve stage-specific settings
    """
    profile = stage_name if stage_name in config.sections() else 'test'
    settings['aws.s3'] = config[profile]['aws.s3']
    settings['aws.cacheClusterEnabled'] = True if config[profile]['aws.apigateway.cacheClusterEnabled'].lower() == 'true' else False
    settings['aws.cacheClusterSize'] = config[profile]['aws.apigateway.cacheClusterSize']
    return settings


@py.test.fixture(scope='session')
def unit_tests_tmp_dir(request):
    t = mkdtemp(prefix='data_service_')
    print('Created tmp test dir {}.'.format(t))

    def teardown():
        # delete sample files created for the unit tests
        if exists(t):
            rmtree(t)
            print('Deleted tmp test dir {}.'.format(t))

    request.addfinalizer(teardown)
    return t


@py.test.fixture(scope='session')
def sample_test_file(unit_tests_tmp_dir):
    filename = join(unit_tests_tmp_dir, 'data_service_testfile.json')

    data = {
        "key1": "value1",
        "key2": "value2"
    }

    with open(filename, 'w') as outfile:
        json.dump(data, outfile)

    return filename