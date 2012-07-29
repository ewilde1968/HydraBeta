import unittest

from google.appengine.api import users
from google.appengine.ext import testbed

from hydramodel import hydrauser
from hydramodel import hydracontent


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

    def testInsertHydraContent(self):
        emailAddr='testInsertHydraContent0@hydrauser.com'
        testEntity = hydrauser.create_hydra_user(users.User(email=emailAddr))

        testName = "testInsertHydraContent"
        testContent = hydracontent.create_hydra_content(hydracontent.HydraContent,
                                    owner=testEntity,
                                    instanceName=testName
                                    )
        testContent.put()

        result = hydracontent.load_hydra_content( testEntity)
        self.assertIsNotNone(result)
        self.assertEqual( len(result), 1)
        self.assertEqual( result[0].owner, testEntity)
        self.assertEqual( result[0].instanceName, testName)

    def testCloneContent(self):
        eAddrs=['testCloneContent0@hydrauser.com',
                    'testCloneContent1@hydrauser.com']
        testEntity = hydrauser.create_hydra_user(users.User(email=eAddrs[0]))
        origPub = hydrauser.create_hydra_user(users.User(email=eAddrs[1]))

        testName = "testCloneContent"
        testContent = hydracontent.create_hydra_content(hydracontent.HydraContent,
                                    owner=origPub,
                                    originalPublisher=origPub,
                                    instanceName=testName
                                    )
        testContent.put()

        result = testContent.clone( testEntity)
        self.assertIsNot( result, testContent)
        self.assertEqual(result.owner, testEntity)
        self.assertEqual(result.originalPublisher, origPub)
        self.assertEqual(result.instanceName, testName)
        self.assertEqual(testContent.owner, origPub)

    def testCloneContentToContent(self):
        eAddr='testCloneContentToContent0@hydrauser.com'
        testEntity = hydrauser.create_hydra_user(users.User(email=eAddr))

        testNames = ['testCloneContentToContent0',
                     'testCloneContentToContent1']
        testContent0 = hydracontent.create_hydra_content(hydracontent.HydraContent,
                                    owner=testEntity,
                                    instanceName=testNames[0]
                                    )
        testContent0.put()
        testContent1 = hydracontent.create_hydra_content(hydracontent.HydraContent,
                                    owner=testEntity,
                                    instanceName=testNames[1]
                                    )
        testContent1.put()

        # clone the content to an item owned by the first content item
        result = testContent1.clone( testContent0)

        self.assertIsNot( result, testContent1)
        self.assertIsNot( result, testContent0)
        self.assertEqual( result.owner, testEntity)
        self.assertEqual( testContent0.owner, testEntity)
        self.assertEqual( testContent1.owner, testEntity)
        self.assertEqual( result.instanceName, testNames[1])
        self.assertEqual( testContent0.instanceName, testNames[0])
        self.assertEqual( testContent1.instanceName, testNames[1])
        self.assertEqual( len(result.contentSet), 0)
        self.assertEqual( len(testContent0.contentSet), 1)
        self.assertEqual( len(testContent1.contentSet), 0)

    def testCloneToContentWithContent(self):
        eAddr='testCloneContentToContent0@hydrauser.com'
        testEntity = hydrauser.create_hydra_user(users.User(email=eAddr))

        testNames = ['testCloneContentToContent0',
                     'testCloneContentToContent1',
                     'subcontent']
        testContent = []
        for t in testNames:
            c = hydracontent.create_hydra_content( hydracontent.HydraContent,
                    owner=testEntity,
                    instanceName=t)
            c.put()
            testContent.append(c)

        # clone the content to an item owned by the first content item
        c0 = testContent[2].clone( testContent[0])
        c1 = testContent[1].clone( testContent[0])

        self.assertIsNot( c0, testContent[2])
        self.assertIsNot( c1, testContent[1])
        self.assertEqual( c0.owner, testEntity)
        self.assertEqual( c1.owner, testEntity)
        self.assertEqual( c0.instanceName, testNames[2])
        self.assertEqual( c1.instanceName, testNames[1])
        self.assertEqual( len(c0.contentSet), 0)
        self.assertEqual( len(c1.contentSet), 0)
        self.assertEqual( len(testContent[0].contentSet), 2)

    def testCloneOfContentWithContent(self):
        eAddr='testCloneContentToContent0@hydrauser.com'
        testEntity = hydrauser.create_hydra_user(users.User(email=eAddr))

        testNames = ['testCloneContentToContent0',
                     'testCloneContentToContent1',
                     'subcontent']
        testContent = []
        for t in testNames:
            c = hydracontent.create_hydra_content( hydracontent.HydraContent,
                    owner=testEntity,
                    instanceName=t)
            c.put()
            testContent.append(c)

        # clone the content to an item owned by the first content item
        c0 = testContent[2].clone( testContent[1])
        c1 = testContent[1].clone( testContent[0])

        self.assertIsNot( c0, testContent[2])
        self.assertIsNot( c1, testContent[1])
        self.assertEqual( c0.owner, testEntity)
        self.assertEqual( c1.owner, testEntity)
        self.assertEqual( c0.instanceName, testNames[2])
        self.assertEqual( c1.instanceName, testNames[1])
        self.assertEqual( len(c0.contentSet), 0)
        self.assertEqual( len(c1.contentSet), 1)
        self.assertEqual( len(testContent[0].contentSet), 1)


if __name__ == '__main__':
    unittest.main()    
