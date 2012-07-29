import unittest

from google.appengine.api import users
from google.appengine.ext import testbed

from hydramodel import hydrauser
from hydramodel import hydracontent
from hydramodel import adventure


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

    def testInsertAdventure(self):
        emailAddr='testInsertAdventure0@hydrauser.com'
        testEntity = hydrauser.create_hydra_user(users.User(email=emailAddr))

        loc = [1.0,2.0,3.0,4.0]
        testContent = hydracontent.create_hydra_content(
                            adventure.Adventure,
                            owner=testEntity,
                            location=loc
                            )
        testContent.put()

        result = hydracontent.load_hydra_content( testEntity)
        self.assertIsNotNone(result)
        self.assertEqual( len(result), 1)
        self.assertEqual( result[0].owner, testEntity)
        self.assertIsInstance( result[0], adventure.Adventure)
        self.assertEqual( len(result[0].location), 4)
        self.assertEqual( result[0].location[0], 1.0)

    def testCloneAdventure(self):
        eAddrs=['testCloneAdventure0@hydrauser.com',
                'testCloneAdventure1@hydrauser.com']
        testEntity = hydrauser.create_hydra_user(users.User(email=eAddrs[0]))
        origPub = hydrauser.create_hydra_user(users.User(email=eAddrs[1]))

        testName = "testCloneAdventure"
        testContent = hydracontent.create_hydra_content(
                            adventure.Adventure,
                            owner=origPub,
                            originalPublisher=origPub,
                            instanceName = testName)
        testContent.put()

        result = testContent.clone( testEntity)
        self.assertIsNot( result, testContent)
        self.assertEqual(result.owner, testEntity)
        self.assertEqual(result.originalPublisher, origPub)
        self.assertEqual(result.instanceName, testName)
        self.assertIsInstance( result, adventure.Adventure)
        

if __name__ == '__main__':
    unittest.main()    
