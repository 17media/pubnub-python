import unittest

from pubnub import utils
from pubnub.endpoints.access.grant import Grant
from pubnub.endpoints.presence.leave import Leave

try:
    from mock import MagicMock
except ImportError:
    from unittest.mock import MagicMock

from pubnub.pubnub import PubNub
from tests.helper import pnconf_pam, sdk_name


class TestGrant(unittest.TestCase):
    def setUp(self):
        self.pubnub = MagicMock(
            spec=PubNub,
            config=pnconf_pam,
            sdk_name=sdk_name,
            timestamp=MagicMock(return_value=123),
            uuid=None
        )
        self.pubnub.uuid = "UUID_GrantUnitTest"
        self.grant = Grant(self.pubnub)

    def test_grant_read_and_write_to_channel(self):
        self.grant.channels('ch').read(True).write(True)

        self.assertEquals(self.grant.build_path(), Grant.GRANT_PATH % pnconf_pam.subscribe_key)

        self.assertEqual(self.grant.build_params(), {
            'pnsdk': sdk_name,
            'uuid': self.pubnub.uuid,
            'r': '1',
            'w': '1',
            'timestamp': '123',
            'channel': 'ch',
            'signature': utils.sign_sha256(pnconf_pam.secret_key,
                                           pnconf_pam.secret_key + "\n" + pnconf_pam.publish_key + "\n" +
                                           "grant\n" + utils.prepare_pam_arguments({
                                               'r': '1',
                                               'w': '1',
                                               'timestamp': 123,
                                               'channel': 'ch',
                                           }))
        })

# TODO: test no any flag are specified
