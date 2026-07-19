"""Utilities for loading the Ethiopia financial inclusion unified dataset.

Includes basic error handling and schema validation so that malformed or missing
data fails loudly with a clear, actionable message rather than propagating silently
into downstream analysis.
"""
from pathlib import Path
import pandas as pd

DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "raw"

REQUIRED_COLUMNS = [
    "record_id", "record_type", "category", "pillar", "indicator", "indicator_code",
    "value_numeric", "observation_date", "source_name", "confidence",
]
VALID_RECORD_TYPES = {"observation", "event", "impact_link", "target"}


class DataLoadError(Exception):
    """Raised when the unified dataset or reference codes cannot be loaded or validated."""


def _require_file(path: Path) -> Path:
    if not path.exists():
        raise DataLoadError(
            f"Expected data file not found at '{path}'. "
            f"Check that the repository's data/raw/ directory is present and untouched."
        )
    return path


def load_unified_data(path: Path = DATA_DIR / "ethiopia_fi_unified_data.csv") -> pd.DataFrame:
    """Load the unified schema dataset (observations, events, impact_links, targets).

    Raises
    ------
    DataLoadError
        If the file is missing, empty, malformed (unparseable dates), or missing
        required columns / contains unrecognized record_type values.
    """
    _require_file(path)

    try:
        df = pd.read_csv(path)
    except pd.errors.EmptyDataError as exc:
        raise DataLoadError(f"'{path}' exists but is empty (no rows/columns).") from exc
    except pd.errors.ParserError as exc:
        raise DataLoadError(f"'{path}' could not be parsed as CSV: {exc}") from exc

    if df.empty:
        raise DataLoadError(f"'{path}' loaded but contains zero rows.")

    missing_cols = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing_cols:
        raise DataLoadError(
            f"'{path}' is missing required column(s): {missing_cols}. "
            f"Found columns: {list(df.columns)}"
        )

    for date_col in ["observation_date", "period_start", "period_end"]:
        if date_col in df.columns:
            try:
                df[date_col] = pd.to_datetime(df[date_col], errors="coerce")
            except (TypeError, ValueError) as exc:
                raise DataLoadError(f"Could not parse '{date_col}' as dates in '{path}': {exc}") from exc

    unknown_types = set(df["record_type"].dropna().unique()) - VALID_RECORD_TYPES
    if unknown_types:
        raise DataLoadError(
            f"'{path}' contains unrecognized record_type value(s): {unknown_types}. "
            f"Expected one of {VALID_RECORD_TYPES}."
        )

    if df["record_id"].duplicated().any():
        dupes = df.loc[df["record_id"].duplicated(), "record_id"].tolist()
        raise DataLoadError(f"'{path}' contains duplicate record_id value(s): {dupes}")

    return df


def load_reference_codes(path: Path = DATA_DIR / "reference_codes.csv") -> pd.DataFrame:
    """Load valid categorical codes for every field.

    Raises
    ------
    DataLoadError
        If the file is missing, empty, or missing the expected 'field'/'code' columns.
    """
    _require_file(path)

    try:
        ref = pd.read_csv(path)
    except pd.errors.EmptyDataError as exc:
        raise DataLoadError(f"'{path}' exists but is empty.") from exc

    if ref.empty:
        raise DataLoadError(f"'{path}' loaded but contains zero rows.")

    missing_cols = [c for c in ("field", "code") if c not in ref.columns]
    if missing_cols:
        raise DataLoadError(f"'{path}' is missing required column(s): {missing_cols}")

    return ref


def _check_loaded(df: pd.DataFrame, name: str) -> None:
    if df is None or not isinstance(df, pd.DataFrame):
        raise DataLoadError(f"{name} expects a pandas DataFrame, got {type(df)}.")
    if "record_type" not in df.columns:
        raise DataLoadError(f"{name} requires a 'record_type' column, which is missing.")


def get_observations(df: pd.DataFrame) -> pd.DataFrame:
    _check_loaded(df, "get_observations")
    return df[df["record_type"] == "observation"].copy()


def get_events(df: pd.DataFrame) -> pd.DataFrame:
    _check_loaded(df, "get_events")
    return df[df["record_type"] == "event"].copy()


def get_impact_links(df: pd.DataFrame) -> pd.DataFrame:
    _check_loaded(df, "get_impact_links")
    return df[df["record_type"] == "impact_link"].copy()


def get_targets(df: pd.DataFrame) -> pd.DataFrame:
    _check_loaded(df, "get_targets")
    return df[df["record_type"] == "target"].copy()


def get_pillar_indicator(df: pd.DataFrame, pillar: str) -> pd.DataFrame:
    """Get observations for a given pillar (e.g. 'ACCESS', 'USAGE').

    Raises
    ------
    DataLoadError
        If `pillar` is not a non-empty string, or the resulting slice is empty
        (likely a typo'd pillar name), so callers get a clear signal instead of a
        silently empty DataFrame downstream.
    """
    if not isinstance(pillar, str) or not pillar.strip():
        raise DataLoadError(f"'pillar' must be a non-empty string, got {pillar!r}.")

    obs = get_observations(df)
    result = obs[obs["pillar"] == pillar].sort_values("observation_date")
    if result.empty:
        available = sorted(obs["pillar"].dropna().unique().tolist())
        raise DataLoadError(
            f"No observations found for pillar='{pillar}'. Available pillars: {available}"
        )
    return result
