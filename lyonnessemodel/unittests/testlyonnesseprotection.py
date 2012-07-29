'''
Created on Jul 23, 2012

@author: ewilde
'''
import unittest

from google.appengine.ext import testbed
from google.appengine.api import users

from hydramodel import hydrauser
from lyonnessemodel import lyonnesseprotection


class DemoTestCase(unittest.TestCase):

    def setUp(self):
        # First, create an instance of the Testbed class.
        self.testbed = testbed.Testbed()
        # Then activate the testbed, which prepares the service stubs for use.
        self.testbed.activate()
        # Next, declare which service stubs you want to use.
        self.testbed.init_datastore_v3_stub()

    def tearDown(self):
        self.testbed.deactivate()

    def testCreateLyonnesseProtection(self):
        emailAddr='testCreateLyonnesseProtection@hydrauser.com'
        testEntity = hydrauser.create_hydra_user(users.User(email=emailAddr))

        testContent = lyonnesseprotection.get_lyonnesseprotection(lyonnesseprotection.LYONESSEPROTECTION_NEGLIGIBLE,
                                                                     owner=testEntity
                                                                     )

        result = lyonnesseprotection.get_lyonnesseprotection(lyonnesseprotection.LYONESSEPROTECTION_NEGLIGIBLE)
        self.assertIsNotNone(result)
        self.assertEqual( result, testContent)
        self.assertEqual( result.value, lyonnesseprotection.LYONESSEPROTECTION_NEGLIGIBLE)
        self.assertEqual( result.valName, 'Negligible')

    def testEnumerateLyonnesseProtection(self):
        emailAddr='testCreateLyonnesseProtection@hydrauser.com'
        testEntity = hydrauser.create_hydra_user(users.User(email=emailAddr))

        result = lyonnesseprotection.get_lyonnesseprotection(lyonnesseprotection.LYONESSEPROTECTION_NEGLIGIBLE,
                                                             owner=testEntity)
        self.assertIsNotNone(result)
        self.assertEqual( result.value, lyonnesseprotection.LYONESSEPROTECTION_NEGLIGIBLE)
        self.assertEqual( result.valName, 'Negligible')
    
        result = lyonnesseprotection.get_lyonnesseprotection(lyonnesseprotection.LYONESSEPROTECTION_TINY)
        self.assertIsNotNone(result)
        self.assertEqual( result.value, lyonnesseprotection.LYONESSEPROTECTION_TINY)
        self.assertEqual( result.valName, 'Tiny')

        result = lyonnesseprotection.get_lyonnesseprotection(lyonnesseprotection.LYONESSEPROTECTION_LIGHT)
        self.assertIsNotNone(result)
        self.assertEqual( result.value, lyonnesseprotection.LYONESSEPROTECTION_LIGHT)
        self.assertEqual( result.valName, 'Light')

        result = lyonnesseprotection.get_lyonnesseprotection(lyonnesseprotection.LYONESSEPROTECTION_MEDIUM)
        self.assertIsNotNone(result)
        self.assertEqual( result.value, lyonnesseprotection.LYONESSEPROTECTION_MEDIUM)
        self.assertEqual( result.valName, 'Medium')

        result = lyonnesseprotection.get_lyonnesseprotection(lyonnesseprotection.LYONESSEPROTECTION_HEAVY)
        self.assertIsNotNone(result)
        self.assertEqual( result.value, lyonnesseprotection.LYONESSEPROTECTION_HEAVY)
        self.assertEqual( result.valName, 'Heavy')

        result = lyonnesseprotection.get_lyonnesseprotection(lyonnesseprotection.LYONESSEPROTECTION_DEVASTATING)
        self.assertIsNotNone(result)
        self.assertEqual( result.value, lyonnesseprotection.LYONESSEPROTECTION_DEVASTATING)
        self.assertEqual( result.valName, 'Devastating')


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()