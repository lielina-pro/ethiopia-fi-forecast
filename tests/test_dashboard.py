"""Smoke tests for the Streamlit dashboard (dashboard/app.py).

Uses Streamlit's official AppTest framework to actually execute the app's script and
navigate every page, catching runtime errors that a plain import/syntax check would miss
(e.g. merge column collisions, tuple-unpacking bugs) -- both of which were caught and fixed
this way during development.
"""
import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

streamlit_testing = pytest.importorskip("streamlit.testing.v1")
from streamlit.testing.v1 import AppTest

APP_PATH = str(PROJECT_ROOT / "dashboard" / "app.py")


@pytest.fixture
def app():
    at = AppTest.from_file(APP_PATH)
    at.run(timeout=30)
    return at


def test_overview_page_loads_without_exceptions(app):
    assert not list(app.exception)
    assert len(app.metric) == 4  # Access, Usage, Mobile Money, P2P/ATM Crossover cards


@pytest.mark.parametrize("page_name", ["Trends", "Forecasts", "Inclusion Projections"])
def test_each_page_loads_without_exceptions(app, page_name):
    app.sidebar.radio[0].set_value(page_name).run(timeout=30)
    assert not list(app.exception), f"{page_name} page raised an exception"


def test_trends_indicator_selectbox_switches_without_error(app):
    app.sidebar.radio[0].set_value("Trends").run(timeout=30)
    for label in ["Digital Payment Adoption Rate", "P2P/ATM Crossover Ratio"]:
        app.selectbox[0].set_value(label).run(timeout=30)
        assert not list(app.exception), f"Switching to '{label}' raised an exception"


def test_forecasts_scenario_selectbox_switches_without_error(app):
    app.sidebar.radio[0].set_value("Forecasts").run(timeout=30)
    for scenario in ["Pessimistic", "Optimistic", "Base"]:
        app.selectbox[0].set_value(scenario).run(timeout=30)
        assert not list(app.exception), f"Switching to '{scenario}' raised an exception"


def test_inclusion_projections_slider_and_scenario_switch_without_error(app):
    app.sidebar.radio[0].set_value("Inclusion Projections").run(timeout=30)
    app.slider[0].set_value(75).run(timeout=30)
    assert not list(app.exception)
    app.selectbox[0].set_value("Pessimistic").run(timeout=30)
    assert not list(app.exception)
