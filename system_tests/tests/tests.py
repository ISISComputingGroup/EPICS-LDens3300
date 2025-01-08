import unittest

from utils.channel_access import ChannelAccess
from utils.ioc_launcher import get_default_ioc_dir
from utils.test_modes import TestModes
from utils.testing import get_running_lewis_and_ioc, skip_if_recsim


DEVICE_PREFIX = "LDNS3300_01"


IOCS = [
    {
        "name": DEVICE_PREFIX,
        "directory": get_default_ioc_dir("LDNS3300"),
        "macros": {},
        "emulator": "ldens3300",
    },
]


TEST_MODES = [TestModes.DEVSIM]


class Ldens3300Tests(unittest.TestCase):
    """
    Tests for the _Device_ IOC.
    """
    def setUp(self):
        self._lewis, self._ioc = get_running_lewis_and_ioc("ldens3300", DEVICE_PREFIX)
        self.ca = ChannelAccess(device_prefix=DEVICE_PREFIX)

    def test_GIVEN_device_disconnected_THEN_pvs_in_error(self):

        with self._lewis.backdoor_simulate_disconnected_device():
            self.ca.assert_that_pv_alarm_is("TEMP", self.ca.Alarms.INVALID, timeout=30)
            self.ca.assert_that_pv_alarm_is("DENSITY", self.ca.Alarms.INVALID, timeout=30)

        self.ca.assert_that_pv_alarm_is("TEMP", self.ca.Alarms.NONE, timeout=30)
        self.ca.assert_that_pv_alarm_is("DENSITY", self.ca.Alarms.NONE, timeout=30)

    def test_GIVEN_device_connected_THEN_pvs_have_values(self):

        temp = 30.0
        dens = 10.0

        self._lewis.backdoor_set_on_device("temperature", temp)
        self._lewis.backdoor_set_on_device("density", dens)

        self.ca.assert_that_pv_is_number("TEMP", temp, tolerance=0.01)
        self.ca.assert_that_pv_is_number("DENSITY", dens, tolerance=0.01)
