'''
Created on Jul 23, 2012

@author: ewilde
'''
import unittest

from google.appengine.ext import testbed
from google.appengine.api import users

from hydramodel import hydrauser
from lyonnessemodel import lyonnessespeed


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

    def testCreateLyonnesseSpeed(self):
        emailAddr='testCreateLyonnesseSpeed@hydrauser.com'
        testEntity = hydrauser.create_hydra_user(users.User(email=emailAddr))

        testContent = lyonnessespeed.get_lyonnessespeed(lyonnessespeed.LYONNESSESPEED_STATIONARY,
                                                        owner=testEntity
                                                        )

        result = lyonnessespeed.get_lyonnessespeed(lyonnessespeed.LYONNESSESPEED_STATIONARY)
        self.assertIsNotNone(result)
        self.assertEqual( result, testContent)
        self.assertEqual( result.value, lyonnessespeed.LYONNESSESPEED_STATIONARY)
        self.assertEqual( result.valName, 'Stationary')

    def testEnumerateLyonnesseSpeed(self):
        emailAddr='testCreateLyonnesseSpeed@hydrauser.com'
        testEntity = hydrauser.create_hydra_user(users.User(email=emailAddr))

        result = lyonnessespeed.get_lyonnessespeed(lyonnessespeed.LYONNESSESPEED_STATIONARY, owner=testEntity)
        self.assertIsNotNone(result)
        self.assertEqual( result.value, lyonnessespeed.LYONNESSESPEED_STATIONARY)
        self.assertEqual( result.valName, 'Stationary')
    
        result = lyonnessespeed.get_lyonnessespeed(lyonnessespeed.LYONNESSESPEED_CREEPING)
        self.assertIsNotNone(result)
        self.assertEqual( result.value, lyonnessespeed.LYONNESSESPEED_CREEPING)
        self.assertEqual( result.valName, 'Creeping')

        result = lyonnessespeed.get_lyonnessespeed(lyonnessespeed.LYONNESSESPEED_PLODDING)
        self.assertIsNotNone(result)
        self.assertEqual( result.value, lyonnessespeed.LYONNESSESPEED_PLODDING)
        self.assertEqual( result.valName, 'Plodding')

        result = lyonnessespeed.get_lyonnessespeed(lyonnessespeed.LYONNESSESPEED_DELIBERATE)
        self.assertIsNotNone(result)
        self.assertEqual( result.value, lyonnessespeed.LYONNESSESPEED_DELIBERATE)
        self.assertEqual( result.valName, 'Deliberate')

        result = lyonnessespeed.get_lyonnessespeed(lyonnessespeed.LYONNESSESPEED_SLOW)
        self.assertIsNotNone(result)
        self.assertEqual( result.value, lyonnessespeed.LYONNESSESPEED_SLOW)
        self.assertEqual( result.valName, 'Slow')

        result = lyonnessespeed.get_lyonnessespeed(lyonnessespeed.LYONNESSESPEED_AVERAGE)
        self.assertIsNotNone(result)
        self.assertEqual( result.value, lyonnessespeed.LYONNESSESPEED_AVERAGE)
        self.assertEqual( result.valName, 'Average')

        result = lyonnessespeed.get_lyonnessespeed(lyonnessespeed.LYONNESSESPEED_ENERGETIC)
        self.assertIsNotNone(result)
        self.assertEqual( result.value, lyonnessespeed.LYONNESSESPEED_ENERGETIC)
        self.assertEqual( result.valName, 'Energetic')

        result = lyonnessespeed.get_lyonnessespeed(lyonnessespeed.LYONNESSESPEED_QUICK)
        self.assertIsNotNone(result)
        self.assertEqual( result.value, lyonnessespeed.LYONNESSESPEED_QUICK)
        self.assertEqual( result.valName, 'Quick')

        result = lyonnessespeed.get_lyonnessespeed(lyonnessespeed.LYONNESSESPEED_SWIFT)
        self.assertIsNotNone(result)
        self.assertEqual( result.value, lyonnessespeed.LYONNESSESPEED_SWIFT)
        self.assertEqual( result.valName, 'Swift')

        result = lyonnessespeed.get_lyonnessespeed(lyonnessespeed.LYONNESSESPEED_IMMEDIATE)
        self.assertIsNotNone(result)
        self.assertEqual( result.value, lyonnessespeed.LYONNESSESPEED_IMMEDIATE)
        self.assertEqual( result.valName, 'Immediate')

        result = lyonnessespeed.get_lyonnessespeed(lyonnessespeed.LYONNESSESPEED_INSTANTANEOUS)
        self.assertIsNotNone(result)
        self.assertEqual( result.value, lyonnessespeed.LYONNESSESPEED_INSTANTANEOUS)
        self.assertEqual( result.valName, 'Instantaneous')

        result = lyonnessespeed.get_lyonnessespeed(lyonnessespeed.LYONNESSESPEED_CHARACTERS)
        self.assertIsNotNone(result)
        self.assertEqual( result.value, lyonnessespeed.LYONNESSESPEED_CHARACTERS)
        self.assertEqual( result.valName, "Character's")


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()