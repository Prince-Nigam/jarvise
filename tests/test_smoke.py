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


if __name__ == "__main__":
    unittest.main()
