'''
Created on Jul 23, 2012

@author: ewilde
'''
import unittest

from google.appengine.ext import testbed
from google.appengine.api import users

from hydramodel import hydrauser
from lyonnessemodel import lyonnesseskilllevel


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

    def testCreateLyonnesseSkillLevel(self):
        emailAddr='testCreateLyonnesseSkillLevel@hydrauser.com'
        testEntity = hydrauser.create_hydra_user(users.User(email=emailAddr))

        testContent = lyonnesseskilllevel.get_lyonnesseskilllevel(lyonnesseskilllevel.LYONNESSESKILLLEVEL_NEOPHYTE,
                                                                  owner=testEntity
                                                                  )

        result = lyonnesseskilllevel.get_lyonnesseskilllevel(lyonnesseskilllevel.LYONNESSESKILLLEVEL_NEOPHYTE)
        self.assertIsNotNone(result)
        self.assertEqual( result, testContent)
        self.assertEqual( result.value, lyonnesseskilllevel.LYONNESSESKILLLEVEL_NEOPHYTE)
        self.assertEqual( result.valName, 'Neophyte')

    def testEnumerateLyonnesseSkillLevel(self):
        emailAddr='testCreateLyonnesseSkillLevel@hydrauser.com'
        testEntity = hydrauser.create_hydra_user(users.User(email=emailAddr))

        result = lyonnesseskilllevel.get_lyonnesseskilllevel(lyonnesseskilllevel.LYONNESSESKILLLEVEL_UNSKILLED, owner=testEntity)
        self.assertIsNotNone(result)
        self.assertEqual( result.value, lyonnesseskilllevel.LYONNESSESKILLLEVEL_UNSKILLED)
        self.assertEqual( result.valName, 'Unskilled')
    
        result = lyonnesseskilllevel.get_lyonnesseskilllevel(lyonnesseskilllevel.LYONNESSESKILLLEVEL_NEOPHYTE)
        self.assertIsNotNone(result)
        self.assertEqual( result.value, lyonnesseskilllevel.LYONNESSESKILLLEVEL_NEOPHYTE)
        self.assertEqual( result.valName, 'Neophyte')

        result = lyonnesseskilllevel.get_lyonnesseskilllevel(lyonnesseskilllevel.LYONNESSESKILLLEVEL_VETERAN)
        self.assertIsNotNone(result)
        self.assertEqual( result.value, lyonnesseskilllevel.LYONNESSESKILLLEVEL_VETERAN)
        self.assertEqual( result.valName, 'Veteran')

        result = lyonnesseskilllevel.get_lyonnesseskilllevel(lyonnesseskilllevel.LYONNESSESKILLLEVEL_SKILLED)
        self.assertIsNotNone(result)
        self.assertEqual( result.value, lyonnesseskilllevel.LYONNESSESKILLLEVEL_SKILLED)
        self.assertEqual( result.valName, 'Skilled')

        result = lyonnesseskilllevel.get_lyonnesseskilllevel(lyonnesseskilllevel.LYONNESSESKILLLEVEL_MASTER)
        self.assertIsNotNone(result)
        self.assertEqual( result.value, lyonnesseskilllevel.LYONNESSESKILLLEVEL_MASTER)
        self.assertEqual( result.valName, 'Master')

        result = lyonnesseskilllevel.get_lyonnesseskilllevel(lyonnesseskilllevel.LYONNESSESKILLLEVEL_SUPERLATIVE)
        self.assertIsNotNone(result)
        self.assertEqual( result.value, lyonnesseskilllevel.LYONNESSESKILLLEVEL_SUPERLATIVE)
        self.assertEqual( result.valName, 'Superlative')


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()