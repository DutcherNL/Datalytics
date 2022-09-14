from . import TestCase


from datalytics.analysis.analysers import *


class TestTempAnalyser(TestCase):

    def setUp(self):
        self.low_temp_analyser = LowerIndoorTemperatureAnalyser()
        self.high_temp_analyser = UpperIndoorTemperatureAnalyser()

    def test_check_low_temp_analyser(self):
        self.assertFalse(self.low_temp_analyser.check(17))
        self.assertTrue(self.low_temp_analyser.check(16))

    def test_check_high_temp_analyser(self):
        self.assertFalse(self.high_temp_analyser.check(25))
        self.assertTrue(self.high_temp_analyser.check(27))


class TestRHAnalyser(TestCase):

    def setUp(self):
        self.low_rh_analyser = LowerIndoorRHAnalyser()
        self.high_rh_analyser = UpperIndoorRHAnalyser()

    def test_check_low_rh_analyser(self):
        self.assertFalse(self.low_rh_analyser.check(26))
        self.assertTrue(self.low_rh_analyser.check(25))

    def test_check_high_rh_analyser(self):
        self.assertFalse(self.high_rh_analyser.check(59))
        self.assertTrue(self.high_rh_analyser.check(60))


class TestCO2Analyser(TestCase):

    def setUp(self):
        self.low_co2_analyser = LowerIndoorCO2Analyser()
        self.high_co2_analyser = UpperIndoorCO2Analyser()

    def test_check_low_co2_analyser(self):
        self.assertFalse(self.low_co2_analyser.check(999))
        self.assertTrue(self.low_co2_analyser.check(1000))

    def test_check_high_co2_analyser(self):
        self.assertFalse(self.high_co2_analyser.check(4999))
        self.assertTrue(self.high_co2_analyser.check(5000))


class TestLuxAnalyser(TestCase):

    def setUp(self):
        self.low_light_analyser = LowIndoorLuxAnalyser()
        self.high_light_analyser = HighIndoorLuxAnalyser()

    def test_check_low_lux_analyser(self):
        self.assertFalse(self.low_light_analyser.check(101))
        self.assertTrue(self.low_light_analyser.check(100))

    def test_check_high_lux_analyser(self):
        self.assertFalse(self.high_light_analyser.check(501))
        self.assertTrue(self.high_light_analyser.check(500))