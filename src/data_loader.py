"""Utilities for loading the Ethiopia financial inclusion unified dataset."""
from pathlib import Path
import pandas as pd

DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "raw"


def load_unified_data(path: Path = DATA_DIR / "ethiopia_fi_unified_data.csv") -> pd.DataFrame:
    """Load the unified schema dataset (observations, events, impact_links, targets)."""
    df = pd.read_csv(path, parse_dates=["observation_date", "period_start", "period_end"])
    return df


def load_reference_codes(path: Path = DATA_DIR / "reference_codes.csv") -> pd.DataFrame:
    """Load valid categorical codes for every field."""
    return pd.read_csv(path)


def get_observations(df: pd.DataFrame) -> pd.DataFrame:
    return df[df["record_type"] == "observation"].copy()


def get_events(df: pd.DataFrame) -> pd.DataFrame:
    return df[df["record_type"] == "event"].copy()


def get_impact_links(df: pd.DataFrame) -> pd.DataFrame:
    return df[df["record_type"] == "impact_link"].copy()


def get_targets(df: pd.DataFrame) -> pd.DataFrame:
    return df[df["record_type"] == "target"].copy()


def get_pillar_indicator(df: pd.DataFrame, pillar: str) -> pd.DataFrame:
    """Get observations for a given pillar (e.g. 'ACCESS', 'USAGE')."""
    obs = get_observations(df)
    return obs[obs["pillar"] == pillar].sort_values("observation_date")
