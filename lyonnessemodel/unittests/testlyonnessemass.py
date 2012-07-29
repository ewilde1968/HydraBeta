'''
Created on Jul 23, 2012

@author: ewilde
'''
import unittest

from google.appengine.ext import testbed
from google.appengine.api import users

from hydramodel import hydrauser
from lyonnessemodel import lyonnessemass


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

    def testCreateLyonnesseMass(self):
        emailAddr='testCreateLyonnesseMass@hydrauser.com'
        testEntity = hydrauser.create_hydra_user(users.User(email=emailAddr))

        testContent = lyonnessemass.get_lyonnessemass(lyonnessemass.LYONNESSEMASS_TINY,
                                                      owner=testEntity
                                                      )

        result = lyonnessemass.get_lyonnessemass(lyonnessemass.LYONNESSEMASS_TINY)
        self.assertIsNotNone(result)
        self.assertEqual( result, testContent)
        self.assertEqual( result.value, lyonnessemass.LYONNESSEMASS_TINY)
        self.assertEqual( result.valName, 'Tiny')

    def testEnumerateLyonnesseMass(self):
        emailAddr='testCreateLyonnesseMass@hydrauser.com'
        testEntity = hydrauser.create_hydra_user(users.User(email=emailAddr))

        result = lyonnessemass.get_lyonnessemass(lyonnessemass.LYONNESSEMASS_NEGLIGIBLE, owner=testEntity)
        self.assertIsNotNone(result)
        self.assertEqual( result.value, lyonnessemass.LYONNESSEMASS_NEGLIGIBLE)
        self.assertEqual( result.valName, 'Negligible')
    
        result = lyonnessemass.get_lyonnessemass(lyonnessemass.LYONNESSEMASS_TINY)
        self.assertIsNotNone(result)
        self.assertEqual( result.value, lyonnessemass.LYONNESSEMASS_TINY)
        self.assertEqual( result.valName, 'Tiny')

        result = lyonnessemass.get_lyonnessemass(lyonnessemass.LYONNESSEMASS_SMALL)
        self.assertIsNotNone(result)
        self.assertEqual( result.value, lyonnessemass.LYONNESSEMASS_SMALL)
        self.assertEqual( result.valName, 'Small')

        result = lyonnessemass.get_lyonnessemass(lyonnessemass.LYONNESSEMASS_AVERAGE)
        self.assertIsNotNone(result)
        self.assertEqual( result.value, lyonnessemass.LYONNESSEMASS_AVERAGE)
        self.assertEqual( result.valName, 'Average')

        result = lyonnessemass.get_lyonnessemass(lyonnessemass.LYONNESSEMASS_LARGE)
        self.assertIsNotNone(result)
        self.assertEqual( result.value, lyonnessemass.LYONNESSEMASS_LARGE)
        self.assertEqual( result.valName, 'Large')

        result = lyonnessemass.get_lyonnessemass(lyonnessemass.LYONNESSEMASS_HUGE)
        self.assertIsNotNone(result)
        self.assertEqual( result.value, lyonnessemass.LYONNESSEMASS_HUGE)
        self.assertEqual( result.valName, 'Huge')


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
    