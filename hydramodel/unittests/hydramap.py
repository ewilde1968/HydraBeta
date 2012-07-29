import unittest

from google.appengine.api import users
from google.appengine.ext import testbed

from hydramodel import hydrauser
from hydramodel import hydracontent
from hydramodel import hydramap


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

    def testInsertHydraMap(self):
        emailAddr='testInsertHydraMap0@hydrauser.com'
        testEntity = hydrauser.create_hydra_user(users.User(email=emailAddr))

        loc = [1.0,2.0,3.0,4.0]
        testContent = hydracontent.create_hydra_content(
                            hydramap.HydraMap,
                            owner=testEntity,
                            location=loc)
        testContent.put()

        result = hydracontent.load_hydra_content( testEntity)
        self.assertIsNotNone(result)
        self.assertEqual( len(result), 1)
        self.assertEqual( result[0].owner, testEntity)
        self.assertIsInstance( result[0], hydramap.HydraMap)
        self.assertEqual( len(result[0].location), 4)
        self.assertEqual( result[0].locations[0], 1.0)

    def testCloneHydraMap(self):
        eAddrs=['testCloneHydraMap0@hydrauser.com',
                'testCloneHydraMap1@hydrauser.com']
        testEntity = hydrauser.create_hydra_user(users.User(email=eAddrs[0]))
        origPub = hydrauser.create_hydra_user(users.User(email=eAddrs[1]))

        testName = "testCloneHydraMap"
        loc = [1.0,2.0,3.0,4.0]
        testContent = hydracontent.create_hydra_content(
                            hydramap.HydraMap,
                            owner=origPub,
                            originalPublisher=origPub,
                            instanceName = testName,
                            location=loc)
        testContent.put()

        result = testContent.clone( testEntity)
        self.assertIsNot( result, testContent)
        self.assertEqual(result.owner, testEntity)
        self.assertEqual(result.originalPublisher, origPub)
        self.assertEqual(result.instanceName, testName)
        self.assertIsInstance( result, hydramap.HydraMap)
        self.assertEqual( len(result.location), 4)
        self.assertEqual( result.location[0], 1.0)
        

if __name__ == '__main__':
    unittest.main()    
