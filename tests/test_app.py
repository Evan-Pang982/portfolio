"""Fast structural smoke tests for the Streamlit portfolio."""

from __future__ import annotations

import site
import unittest
from pathlib import Path


ROOT = Path(__file__).parents[1]
LOCAL_TEST_PACKAGES = ROOT / "tmp" / "site-packages"
if LOCAL_TEST_PACKAGES.exists():
    site.addsitedir(str(LOCAL_TEST_PACKAGES))

from streamlit.testing.v1 import AppTest  # noqa: E402


class PortfolioSmokeTest(unittest.TestCase):
    def setUp(self) -> None:
        self.app = AppTest.from_file(str(ROOT / "streamlit_app.py"), default_timeout=15).run()

    def assert_clean(self) -> None:
        self.assertEqual([], list(self.app.exception))

    def test_home_loads(self) -> None:
        self.assert_clean()
        self.assertEqual("Home", self.app.radio[0].value)

    def test_every_navigation_section_loads(self) -> None:
        for page in ["Role & Projects", "Evidence", "KSA", "Reflection", "Contact"]:
            self.app.radio[0].set_value(page).run()
            self.assert_clean()
            self.assertEqual(page, self.app.radio[0].value)


if __name__ == "__main__":
    unittest.main(verbosity=2)
