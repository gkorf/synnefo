from synnefo.lib.settings import setup
from synnefo.lib.settings.setup import Setting
import unittest


class CycleDetectionTests(unittest.TestCase):
    def run_settings_test(self, test_settings):
        setup.reset_all_catalogs()
        setup.initialize_settings(test_settings)
        settings = setup.Catalogs['settings']
        setup.assign_dependents(settings)
        setup.assign_configured_depths(settings)

    def test_01_should_be_ok(self):
        test_settings = {
            'ONE': Setting(dependencies=[]),
            'TWO': Setting(dependencies=[]),
            'THREE': Setting(dependencies=['ONE']),
            'FOUR': Setting(dependencies=['ONE', 'TWO']),
            'FIVE': Setting(dependencies=['THREE']),
            'SIX': Setting(dependencies=['FIVE', 'FOUR']),
            'SEVEN': Setting(dependencies=['FIVE', 'FOUR']),
        }
        self.run_settings_test(test_settings)

    def test_02_connected_cycle(self):
        test_settings = {
            'ONE': Setting(dependencies=[]),
            'TWO': Setting(dependencies=[]),
            'THREE': Setting(dependencies=['ONE', 'SEVEN']),
            'FOUR': Setting(dependencies=['ONE', 'TWO']),
            'FIVE': Setting(dependencies=['THREE']),
            'SIX': Setting(dependencies=['FIVE', 'FOUR']),
            'SEVEN': Setting(dependencies=['FIVE', 'FOUR']),
        }
        self.assertRaises(setup.CycleError,
                          self.run_settings_test, test_settings)

    def test_03_disconnected_cycle(self):
        test_settings = {
            'ONE': Setting(dependencies=[]),
            'TWO': Setting(dependencies=[]),
            'THREE': Setting(dependencies=['ONE']),
            'FOUR': Setting(dependencies=['ONE', 'TWO']),
            'FIVE': Setting(dependencies=['SIX']),
            'SIX': Setting(dependencies=['SEVEN']),
            'SEVEN': Setting(dependencies=['FIVE']),
        }
        self.assertRaises(setup.CycleError,
                          self.run_settings_test, test_settings)

    def test_04_self_cycle(self):
        test_settings = {
            'ONE': Setting(dependencies=[]),
            'TWO': Setting(dependencies=[]),
            'THREE': Setting(dependencies=['ONE']),
            'FOUR': Setting(dependencies=['ONE', 'TWO']),
            'FIVE': Setting(dependencies=['SIX']),
            'SIX': Setting(dependencies=['SEVEN']),
            'SEVEN': Setting(dependencies=['SEVEN']),
        }
        self.assertRaises(setup.CycleError,
                          self.run_settings_test, test_settings)

    def test_04_disconnected_self_cycle(self):
        test_settings = {
            'ONE': Setting(dependencies=[]),
            'TWO': Setting(dependencies=[]),
            'THREE': Setting(dependencies=['ONE']),
            'FOUR': Setting(dependencies=['ONE', 'TWO']),
            'FIVE': Setting(dependencies=['SIX']),
            'SIX': Setting(dependencies=['FOUR']),
            'SEVEN': Setting(dependencies=['SEVEN']),
        }
        self.assertRaises(setup.CycleError,
                          self.run_settings_test, test_settings)


if __name__ == '__main__':
    unittest.main()
