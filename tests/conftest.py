"""
Jupyter SCAD
Copyright (C) 2023 Jennifer Reiber Kyle

This program is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with
this program. If not, see <https://www.gnu.org/licenses/>.
"""
import logging
from pathlib import Path

import pytest

LOGGER = logging.getLogger(__name__)

TEST_DATA_PATH = Path(__file__).parent.absolute() / "data"


@pytest.fixture
def test_data():
    LOGGER.info(TEST_DATA_PATH)

    def f(filename):
        return TEST_DATA_PATH / filename

    return f
