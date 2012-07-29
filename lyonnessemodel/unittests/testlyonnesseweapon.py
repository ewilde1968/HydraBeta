'''
Created on Jul 25, 2012

@author: ewilde
'''
import unittest

from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext import testbed

from hydramodel import hydrauser
from hydramodel import hydracontent

from lyonnessemodel import lyonnessespeed
from lyonnessemodel import lyonnesseweapon


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

    def testInsertLyonnesseWeapon(self):
        emailAddr='testInsertLyonnesseWeapon@hydrauser.com'
        testEntity = hydrauser.create_hydra_user(users.User(email=emailAddr))

        testWS = lyonnessespeed.get_lyonnessespeed(lyonnessespeed.LYONNESSESPEED_AVERAGE, testEntity)
        testPS = lyonnessespeed.get_lyonnessespeed(lyonnessespeed.LYONNESSESPEED_CHARACTERS)
        testName = 'Battle Axe'
        testContent = hydracontent.create_hydra_content(lyonnesseweapon.LyonnesseWeapon,
                                                        owner=testEntity,
                                                        weaponSpeed=testWS,
                                                        poisedSpeed=testPS,
                                                        length=8,
                                                        instanceName=testName
                                                        )
        testContent.put()
 
        result = hydracontent.load_hydra_content( testEntity)
        self.assertIsNotNone(result)

        result = db.get( testContent.key())
        self.assertIsNotNone(result)
        self.assertIsInstance( result, lyonnesseweapon.LyonnesseWeapon)
        self.assertEqual( result.weaponSpeed, testWS)
        self.assertEqual( result.poisedSpeed, testPS)
        self.assertEqual( result.instanceName, testName)
        self.assertEqual( result.length, 8)
        self.assertEqual( result, testContent)  # test __eq__
        

    def testCloneLyonnesseWeapon(self):
        eAddrs=['testCloneLyonnesseWeapon0@hydrauser.com',
                'testCloneLyonnesseWeapon1@hydrauser.com']
        testEntity = hydrauser.create_hydra_user(users.User(email=eAddrs[0]))
        origPub = hydrauser.create_hydra_user(users.User(email=eAddrs[1]))

        testWS = lyonnessespeed.get_lyonnessespeed(lyonnessespeed.LYONNESSESPEED_AVERAGE, origPub)
        testPS = lyonnessespeed.get_lyonnessespeed(lyonnessespeed.LYONNESSESPEED_CHARACTERS)
        testName = 'Battle Axe'
        testContent = hydracontent.create_hydra_content(lyonnesseweapon.LyonnesseWeapon,
                                                        owner=origPub,
                                                        originalPublisher=origPub,
                                                        weaponSpeed=testWS,
                                                        poisedSpeed=testPS,
                                                        length=8,
                                                        instanceName=testName
                                                        )
        testContent.put()

        result = testContent.clone( testEntity)
        self.assertIsNotNone(result)
        self.assertIsInstance( result, lyonnesseweapon.LyonnesseWeapon)
        self.assertEqual( result.weaponSpeed, testWS)
        self.assertEqual( result.poisedSpeed, testPS)
        self.assertEqual( result.instanceName, testName)
        self.assertEqual( result.length, 8)
        

if __name__ == '__main__':
    unittest.main()    
