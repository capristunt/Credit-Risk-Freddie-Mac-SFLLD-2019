# Credit Risk on Freddie Mac 2019: From PD to Portfolio Value

How much is a calibrated risk score worth to a mortgage book? This project scores 49,946 loans from the 2019 vintage of Freddie Mac's Single-Family Loan-Level Dataset, turns each predicted probability of default into a hold-or-drop decision through explicit loss and margin assumptions, and measures the result in dollars against FICO-floor policies.

**[Read the case study](reports/case_study.html)**

## Headline results

| | |
|---|---|
| Selected model | Logistic regression on banded attributes, chosen over LightGBM by a rule fixed before testing (test AUC 0.732 vs 0.726, difference within sampling noise) |
| Decision rule | Hold a loan while PD < 10.7%, the break-even implied by a 25% LGD and a 1.5% annual margin over two years |
| Scenario value lift | **+\$2.7M** on \$3.84B of test balance, about 7 bp, 95% bootstrap interval \$1.1M to \$4.4M |
| Versus FICO floors | At matched selection rates, the score beats every tested FICO cutoff from 660 to 740; looser floors are indistinguishable |
| Calibration | Mean predicted PD 4.55% vs 4.59% observed on the test set, no recalibration needed |

![Observed 90+ DPD rate by FICO and LTV band](figures/02_bivariate_fico_ltv.png)

*Risk climbs along both axes: a sub-660 borrower with a large down payment is riskier than a 780+ borrower with less than 5% down. A single FICO floor cannot capture that, which is where the score adds value.*

## Repository structure

```
├── notebooks/
│   ├── 01_data_preparation.ipynb                 # raw files to a leakage-safe modelling table, 24-month 90+ DPD label
│   ├── 02_eda_business_insights.ipynb            # portfolio profile, segment risk, interactions, label sensitivity
│   ├── 03_modeling_and_business_decision.ipynb   # logistic vs LightGBM, calibration, cutoff economics, FICO benchmark
│   └── 04_case_study.ipynb                       # narrative summary, exported to HTML
├── figures/                                      # charts saved by notebooks 02 and 03
├── reports/
│   └── case_study.html                           # nbconvert export of notebook 04
└── data/                                         # not versioned, see below
```

## Reproduce

1. **Get the data.** Register for free on the [Freddie Mac Single-Family Loan-Level Dataset](https://www.freddiemac.com/research/datasets/sf-loanlevel-dataset) page and download the 2019 sample origination and performance files into `data/raw/`.
2. **Install the environment** (Python 3.12):
   ```bash
   python -m venv .venv && source .venv/bin/activate
   pip install -e .
   ```
3. **Run the notebooks in order**, 01 to 03. Each one reads the output of the previous one and saves its figures to `figures/`.
4. **Export the case study:**
   ```bash
   jupyter nbconvert notebooks/04_case_study.ipynb --to html --no-input --execute \
       --output-dir reports --output case_study
   ```

## Scope and limits

The data contain loans already acquired by Freddie Mac, so the results describe portfolio selection within an acquired book, not approval decisions on applicants. The label is a recorded 90+ DPD event over a window that overlaps the pandemic, not a realized loss. Dollar figures are scenario values under assumed economics, validated on a single vintage. Section 7 of the case study details each limit and the next steps.

---

Théophile Jennepin · [Qaventra Data](https://qaventra-data.com) · [GitHub](https://github.com/capristunt)