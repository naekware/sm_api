import unittest
from sm_api.SteamMarketItem import SteamMarketItem


class TestSMI(unittest.TestCase):
    def test_smi(self):
        smi = SteamMarketItem(730, "M4A4 | Buzz Kill (Minimal Wear)")
        self.assertTrue(any(smi.prices))
