import unittest
from healthchecks import healthchecks

class HealthchecksTests(unittest.TestCase):

    def test_run(self):
        checks = [
            healthchecks.Healthcheck('redis')
        ]
        hc = healthchecks.Healthchecks(checks)
        self.assertTrue(hc.run())


if __name__ == '__main__':
    unittest.main()
