# -*- coding:utf-8 -*-
from __future__ import with_statement
import sys
import unittest2
import httplib

try:
    import simplejson as json
except ImportError:
    import json

from werkzeug.test import Client
from werkzeug.wrappers import BaseResponse
import libcloud
from libcloud.loadbalancer.base import Algorithm
from libcloud.test.loadbalancer.test_rackspace import RackspaceLBMockHttp, \
    RackspaceLBDriver

from libcloud_rest.api.versions import versions as rest_versions
from libcloud_rest.application import LibcloudRestApp
from tests.file_fixtures import DNSFixtures


class RackspaceUSTests(unittest2.TestCase):
    def setUp(self):
        self.url_tmpl = rest_versions[libcloud.__version__] +\
            '/loadbalancer/RACKSPACE_US/%s?test=1'
        self.client = Client(LibcloudRestApp(), BaseResponse)
        self.fixtures = DNSFixtures('rackspace_us')
        self.headers = {'x-auth-user': 'user', 'x-api-key': 'key'}
        RackspaceLBMockHttp.type = None

    def test_list_protocols(self):
        url = self.url_tmpl % ('protocols')
        resp = self.client.get(url, headers=self.headers)
        protocols = json.loads(resp.data)
        self.assertEqual(len(protocols), 10)
        self.assertIn('http', protocols)
        self.assertEqual(resp.status_code, httplib.OK)

    def test_ex_list_protocols_with_default_ports(self):
        url = self.url_tmpl % ('ex_list_protocols_with_default_ports')
        resp = self.client.post(url, headers=self.headers,
                                content_type='application/json')
        protocols = json.loads(resp.data)
        self.assertEqual(len(protocols), 10)
        self.assertIn(['http', 80], protocols)
        self.assertEqual(resp.status_code, httplib.OK)

    def test_list_supported_algorithms(self):
        url = self.url_tmpl % ('algorithms')
        resp = self.client.get(url, headers=self.headers)
        algorithms = json.loads(resp.data)
        self.assertTrue(Algorithm.RANDOM in algorithms)
        self.assertTrue(Algorithm.ROUND_ROBIN in algorithms)
        self.assertTrue(Algorithm.LEAST_CONNECTIONS in algorithms)
        self.assertTrue(Algorithm.WEIGHTED_ROUND_ROBIN in algorithms)
        self.assertTrue(Algorithm.WEIGHTED_LEAST_CONNECTIONS in algorithms)
        self.assertEqual(resp.status_code, httplib.OK)

    def test_ex_list_algorithms(self):
        url = self.url_tmpl % ('ex_list_algorithm_names')
        resp = self.client.post(url, headers=self.headers,
                                content_type='application/json')
        algorithms = json.loads(resp.data)
        self.assertIn("RANDOM", algorithms)
        self.assertIn("ROUND_ROBIN", algorithms)
        self.assertIn("LEAST_CONNECTIONS", algorithms)
        self.assertIn("WEIGHTED_ROUND_ROBIN", algorithms)
        self.assertIn("WEIGHTED_LEAST_CONNECTIONS", algorithms)
        self.assertEqual(resp.status_code, httplib.OK)

    def test_list_balancers(self):
        url = self.url_tmpl % ('balancers')
        resp = self.client.get(url, headers=self.headers)
        balancers = json.loads(resp.data)
        self.assertEquals(len(balancers), 2)
        self.assertEquals(balancers[0]['name'], "test0")
        self.assertEquals(balancers[0]['id'], "8155")
        self.assertEquals(balancers[0]['port'], 80)
        self.assertEquals(balancers[0]['ip'], "1.1.1.25")
        self.assertEquals(balancers[1]['name'], "test1")
        self.assertEquals(balancers[1]['id'], "8156")
        self.assertEqual(resp.status_code, httplib.OK)
