"""Loaders for the Freddie Mac Single Family Loan-Level Dataset (Standard layout)."""

from pathlib import Path

import pandas as pd


# Origination file layout
_ORIG_COLUMNS = [
    "credit_score",
    "first_payment_date",
    "first_time_homebuyer_flag",
    "maturity_date",
    "msa",
    "mi_pct",
    "num_units",
    "occupancy_status",
    "ocltv",
    "dti",
    "original_upb",
    "ltv",
    "original_interest_rate",
    "channel",
    "prepayment_penalty_flag",
    "amortization_type",
    "property_state",
    "property_type",
    "postal_code",
    "loan_sequence_number",
    "loan_purpose",
    "original_loan_term",
    "number_of_borrowers",
    "seller_name",
    "servicer_name",
    "super_conforming_flag",
    "pre_harp_loan_sequence_number",
    "program_indicator",
    "harp_indicator",
    "property_valuation_method",
    "interest_only_indicator",
]

_ORIG_DTYPES = {
    "credit_score": "float64",
    "first_payment_date": "Int64",
    "first_time_homebuyer_flag": "str",
    "maturity_date": "Int64",
    "msa": "Int64",
    "mi_pct": "float64",
    "num_units": "float64",
    "occupancy_status": "str",
    "ocltv": "float64",
    "dti": "float64",
    "original_upb": "float64",
    "ltv": "float64",
    "original_interest_rate": "float64",
    "channel": "str",
    "prepayment_penalty_flag": "str",
    "amortization_type": "str",
    "property_state": "str",
    "property_type": "str",
    "postal_code": "str",
    "loan_sequence_number": "str",
    "loan_purpose": "str",
    "original_loan_term": "float64",
    "number_of_borrowers": "float64",
    "seller_name": "str",
    "servicer_name": "str",
    "super_conforming_flag": "str",
    "pre_harp_loan_sequence_number": "str",
    "program_indicator": "str",
    "harp_indicator": "str",
    "property_valuation_method": "str",
    "interest_only_indicator": "str",
}

_PERF_COLUMNS_OF_INTEREST = {
    0: "loan_sequence_number",
    1: "monthly_reporting_period",
    3: "current_loan_delinquency_status",
    4: "loan_age",
    8: "zero_balance_code",
    9: "zero_balance_effective_date",
}

_PERF_DTYPES = {
    "loan_sequence_number": "str",
    "monthly_reporting_period": "Int64",
    "current_loan_delinquency_status": "str",
    "loan_age": "Int64",
    "zero_balance_code": "str",
    "zero_balance_effective_date": "Int64",
}


class FreddieMacLoader:
    """Load raw Freddie Mac SFLLD files into pandas DataFrames.

    The loader does not clean, filter, or transform the data. It only
    handles the mechanics of reading pipe-separated files without headers
    and applying the correct column names and dtypes from the Freddie Mac
    Standard Dataset layout.

    Parameters
    ----------
    data_raw : Path
        Directory containing the raw .txt files.
    """

    def __init__(self, data_raw: Path):
        self.data_raw = Path(data_raw)

    def load_origination(self, filename: str = "sample_orig_2019.txt") -> pd.DataFrame:
        """Load the origination file. One row per loan, 31 columns."""
        path = self.data_raw / filename
        return pd.read_csv(
            path,
            sep="|",
            header=None,
            names=_ORIG_COLUMNS,
            dtype=_ORIG_DTYPES,
            na_values=[""],
            keep_default_na=True,
        )

    def load_performance(self, filename: str = "sample_perf_2019.txt") -> pd.DataFrame:
        """Load the monthly performance file. One row per loan per observation month.
        
        Only six columns are loaded (see _PERF_COLUMNS_OF_INTEREST): the join key,
        the reporting period, the delinquency status, the loan age, and the two
        zero-balance columns. Other columns from the Standard Dataset layout are
        skipped at read time to save memory.
        """
        path = self.data_raw / filename
        return pd.read_csv(
            path,
            sep="|",
            header=None,
            usecols=list(_PERF_COLUMNS_OF_INTEREST.keys()),
            names=[_PERF_COLUMNS_OF_INTEREST[i] for i in sorted(_PERF_COLUMNS_OF_INTEREST.keys())],
            dtype=_PERF_DTYPES,
            na_values=[""],
            keep_default_na=True,
        )