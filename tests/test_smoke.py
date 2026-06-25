import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))


class SmokeTests(unittest.TestCase):
    def test_imports(self):
        import main
        import engine.command as command
        import engine.features as features

        self.assertTrue(callable(command.speak))
        self.assertTrue(callable(features.playAssistantSound))

    def test_safe_call_missing_eel_function(self):
        import main

        self.assertFalse(main.safe_call_js_function('missing_function'))


if __name__ == "__main__":
    unittest.main()
