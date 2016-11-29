from testing_config import BaseTestConfig
from application.models import User, Friendship, FriendMessage, PartyMessage
from application.models import Party
from application.models import PartyUser
import datetime, time
# from application.models import UberRide

class TestModels(BaseTestConfig):
    def test_get_user_with_email_and_password(self):
        self.assertTrue(
                User.get_user_with_email_and_password(
                        self.default_user["email"],
                        self.default_user["password"])
        )
    def test_get_avatar_for_user(self):
        self.assertTrue(
                User.get_avatar_for_useremail(
                        self.default_user["email"])
        )
        self.assertFalse(
                User.get_avatar_for_useremail(
                        "fake@fake.com")
        )
        self.assertTrue(
                User.get_avatar_for_username(
                        self.default_user["username"])
        )
        self.assertFalse(
                User.get_avatar_for_username(
                        "fake")
        )

    def test_get_friendship_with_user_ids(self):
        self.assertTrue(
            Friendship.get_friendship_with_user_ids(self.default_user["id"], self.d_user_two["id"])
        )
        self.assertTrue("Friendship" in repr(Friendship.get_friendship_with_user_ids(self.default_user["id"], self.d_user_two["id"])))
        self.assertFalse(
            Friendship.get_friendship_with_user_ids(10101, 10102)
        )
    def test_get_all_friendship_of_user(self):
        self.assertTrue(
            Friendship.get_all_friendship_of_user(self.default_user["id"])
        )
        self.assertFalse(
            Friendship.get_all_friendship_of_user(self.d_user_three["id"])
        )

    def test_getMyParties(self):
        self.assertTrue(
                Party.getMyParties(self.default_user["id"])
        )
        self.assertFalse(Party.getMyParties(self.d_user_two["id"]))
        for party in Party.getMyParties(self.default_user["id"]):
            self.assertTrue("Party" in repr(party))
    def test_getPartyUsers(self):
        party = Party.query.filter_by(ownerID=self.default_user["id"], partyName=self.default_party["partyName"]).first()
        self.assertTrue(PartyUser.getPartyUsers(party.partyID))
        self.assertFalse(PartyUser.getPartyUsers(10101))

    def test_add_and_get_friendMessage(self):
        now = datetime.datetime.now().strftime('%H:%M:%S')
        sender = self.default_user["username"]
        receiver = self.d_user_two["username"]
        messagetext = "hello"
        res1 = FriendMessage.add_friendMessage("nulluser", receiver, now, messagetext)
        self.assertEqual(res1, "empty sender user")
        res2 = FriendMessage.add_friendMessage(sender, "nulluser", now, messagetext)
        self.assertEqual(res2, "empty receiver user")
        result = FriendMessage.add_friendMessage(sender, receiver, now, messagetext)
        self.assertEqual(result, "success")
        result = FriendMessage.getFriendMessages(sender, receiver)
        self.assertTrue(result)

    def test_add_and_get_partyMessage(self):
        now = datetime.datetime.now().strftime('%H:%M:%S')
        sender = self.default_user
        party = self.default_party
        messagetext = "hello"
        res = PartyMessage.add_partyMessage(party["partyID"], sender["username"], now, messagetext)
        self.assertEqual(res, "success")
        res2 = PartyMessage.add_partyMessage(party["partyID"], sender["username"], now, "hello again")
        result = PartyMessage.getPartyMessages(party["partyID"])
        self.assertTrue(len(result)==2)
        print(result)

"""
    def test_getRides(self):
        self.assertTrue(
                UberRide.getRides(self.default_user["id"])
        )
        self.assertFalse(UberRide.getRides(self.d_user_two["id"]))
        for ride in UberRide.getRides(self.default_user["id"]):
            self.assertTrue("UberRide" in repr(ride))
"""

"""
    def test_PartyMessages(self):
        self.assertTrue(
                PartyMessage(self.default_party["partyID"],self.default_user["id"],"2016-11-08 00:00:00","My Message")
        )

    def test_getPartyMessages(self):
        self.assertTrue(
                PartyMessage.getPartyMessages(self.default_party["partyID"])
        )
"""
