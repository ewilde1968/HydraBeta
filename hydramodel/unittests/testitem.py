import unittest

from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext import testbed

from hydramodel import hydrauser
from hydramodel import hydracontent
from hydramodel import item


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

    def testInsertItem(self):
        emailAddr='testInsertItem0@hydrauser.com'
        testEntity = hydrauser.create_hydra_user(users.User(email=emailAddr))

        dummy = hydracontent.create_hydra_content(
            item.Item,
            owner=testEntity,
            instanceName='dummy')
        dummy.put()

        testContent = hydracontent.create_hydra_content(
                            item.Item,
                            mass = dummy,
                            owner=testEntity)
        testContent.put()

        result = hydracontent.load_hydra_content( testEntity)
        self.assertIsNotNone(result)
        self.assertEqual( len(result), 2)

        result = db.get( testContent.key())
        self.assertEqual( result.owner, testEntity)
        self.assertIsInstance( result, item.Item)
        self.assertEqual( result.mass, dummy)

    def testCloneItem(self):
        eAddrs=['testCloneItem0@hydrauser.com',
                'testCloneItem1@hydrauser.com']
        testEntity = hydrauser.create_hydra_user(users.User(email=eAddrs[0]))
        origPub = hydrauser.create_hydra_user(users.User(email=eAddrs[1]))

        dummy = hydracontent.create_hydra_content(
            hydracontent.HydraContent,
            owner=testEntity,
            instanceName='dummy')
        dummy.put()

        testName = "testCloneItem"
        testContent = hydracontent.create_hydra_content(
                            item.Item,
                            mass = dummy,
                            owner=origPub,
                            originalPublisher=origPub,
                            instanceName = testName)
        testContent.put()

        result = testContent.clone( testEntity)
        self.assertIsNot( result, testContent)
        self.assertEqual(result.owner, testEntity)
        self.assertEqual(result.originalPublisher, origPub)
        self.assertEqual(result.instanceName, testName)
        self.assertIsInstance( result, item.Item)
        self.assertEqual( result.mass, dummy)
        

if __name__ == '__main__':
    unittest.main()    
