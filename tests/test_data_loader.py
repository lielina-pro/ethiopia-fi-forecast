import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.data_loader import (
    load_unified_data,
    load_reference_codes,
    get_observations,
    get_events,
    get_impact_links,
    get_targets,
)


def test_load_unified_data_has_expected_record_types():
    df = load_unified_data()
    assert set(df["record_type"].unique()) == {"observation", "event", "impact_link", "target"}


def test_no_duplicate_record_ids():
    df = load_unified_data()
    assert df["record_id"].is_unique


def test_impact_links_have_valid_parent_id():
    df = load_unified_data()
    events = set(get_events(df)["record_id"])
    links = get_impact_links(df)
    assert links["parent_id"].isin(events).all()


def test_reference_codes_load():
    ref = load_reference_codes()
    assert "field" in ref.columns
    assert "code" in ref.columns


def test_observation_pillars_are_valid():
    df = load_unified_data()
    ref = load_reference_codes()
    valid_pillars = set(ref[ref["field"] == "pillar"]["code"])
    obs = get_observations(df)
    assert obs["pillar"].dropna().isin(valid_pillars).all()


def test_targets_exist():
    df = load_unified_data()
    targets = get_targets(df)
    assert len(targets) == 3
