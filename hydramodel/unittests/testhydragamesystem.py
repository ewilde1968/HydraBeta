'''
Created on Jul 23, 2012

@author: ewilde
'''
import unittest

from google.appengine.api import users
from google.appengine.ext import testbed

from hydramodel import hydrauser
from hydramodel import hydracontent
from hydramodel import hydragamesystem


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

    def testInsertHydraGameSystem(self):
        emailAddr='testInsertHydraGameSystem@hydrauser.com'
        testEntity = hydrauser.create_hydra_user(users.User(email=emailAddr))

        testName = '1.0'
        testContent = hydracontent.create_hydra_content(
                            hydragamesystem.HydraGameSystem,
                            owner=testEntity,
                            version=testName
                            )
        testContent.put()

        result = hydracontent.load_hydra_content( testEntity)
        self.assertIsNotNone(result)
        self.assertEqual( len(result), 1)
        self.assertEqual( result[0].owner, testEntity)
        self.assertIsInstance( result[0], hydragamesystem.HydraGameSystem)
        self.assertEqual( result[0].version, testName)

    def testCloneGameSystem(self):
        eAddrs=['testCloneGameSystem0@hydrauser.com',
                'testCloneGameSystem1@hydrauser.com']
        testEntity = hydrauser.create_hydra_user(users.User(email=eAddrs[0]))
        origPub = hydrauser.create_hydra_user(users.User(email=eAddrs[1]))

        testName = "testCloneGameSystem"
        testVersion = "1.1"
        testContent = hydracontent.create_hydra_content(
                            hydragamesystem.HydraGameSystem,
                            owner=origPub,
                            originalPublisher=origPub,
                            instanceName = testName,
                            version=testVersion
                            )
        testContent.put()

        result = testContent.clone( testEntity)
        self.assertIsNot( result, testContent)
        self.assertEqual(result.owner, testEntity)
        self.assertEqual(result.originalPublisher, origPub)
        self.assertEqual(result.instanceName, testName)
        self.assertIsInstance( result, hydragamesystem.HydraGameSystem)
        self.assertEqual(result.version, testVersion)
        

if __name__ == '__main__':
    unittest.main()    
