import sys
from pathlib import Path

import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.data_loader import (
    load_unified_data,
    load_reference_codes,
    get_observations,
    get_events,
    get_impact_links,
    get_targets,
    get_pillar_indicator,
    DataLoadError,
)


# ---- Happy-path tests ----

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


def test_get_pillar_indicator_returns_sorted_access_observations():
    df = load_unified_data()
    access = get_pillar_indicator(df, "ACCESS")
    assert len(access) > 0
    assert access["observation_date"].is_monotonic_increasing


# ---- Error-handling tests (missing/malformed data) ----

def test_load_unified_data_missing_file_raises_clear_error(tmp_path):
    missing_path = tmp_path / "does_not_exist.csv"
    with pytest.raises(DataLoadError, match="not found"):
        load_unified_data(path=missing_path)


def test_load_unified_data_empty_file_raises_clear_error(tmp_path):
    empty_path = tmp_path / "empty.csv"
    empty_path.write_text("")
    with pytest.raises(DataLoadError, match="empty"):
        load_unified_data(path=empty_path)


def test_load_unified_data_missing_required_column_raises_clear_error(tmp_path):
    bad_path = tmp_path / "missing_cols.csv"
    pd.DataFrame({"record_id": ["REC_0001"], "record_type": ["observation"]}).to_csv(bad_path, index=False)
    with pytest.raises(DataLoadError, match="missing required column"):
        load_unified_data(path=bad_path)


def test_load_unified_data_unknown_record_type_raises_clear_error(tmp_path):
    bad_path = tmp_path / "bad_type.csv"
    row = {c: None for c in [
        "record_id", "record_type", "category", "pillar", "indicator", "indicator_code",
        "value_numeric", "observation_date", "source_name", "confidence",
    ]}
    row.update({"record_id": "REC_0001", "record_type": "not_a_real_type"})
    pd.DataFrame([row]).to_csv(bad_path, index=False)
    with pytest.raises(DataLoadError, match="unrecognized record_type"):
        load_unified_data(path=bad_path)


def test_load_unified_data_duplicate_record_id_raises_clear_error(tmp_path):
    bad_path = tmp_path / "dupes.csv"
    row = {c: None for c in [
        "record_id", "record_type", "category", "pillar", "indicator", "indicator_code",
        "value_numeric", "observation_date", "source_name", "confidence",
    ]}
    row.update({"record_id": "REC_0001", "record_type": "observation"})
    pd.DataFrame([row, row]).to_csv(bad_path, index=False)
    with pytest.raises(DataLoadError, match="duplicate record_id"):
        load_unified_data(path=bad_path)


def test_load_reference_codes_missing_file_raises_clear_error(tmp_path):
    missing_path = tmp_path / "nope.csv"
    with pytest.raises(DataLoadError, match="not found"):
        load_reference_codes(path=missing_path)


def test_get_observations_rejects_non_dataframe():
    with pytest.raises(DataLoadError, match="pandas DataFrame"):
        get_observations(None)


def test_get_pillar_indicator_rejects_empty_pillar():
    df = load_unified_data()
    with pytest.raises(DataLoadError, match="non-empty string"):
        get_pillar_indicator(df, "")


def test_get_pillar_indicator_unknown_pillar_raises_clear_error():
    df = load_unified_data()
    with pytest.raises(DataLoadError, match="No observations found"):
        get_pillar_indicator(df, "NOT_A_REAL_PILLAR")
