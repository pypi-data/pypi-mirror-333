# Copyright 2024-2025 MOSTLY AI
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging
from pathlib import Path

import numpy as np
import pandas as pd

from mostlyai.qa import _accuracy, _sampling, _similarity, _html_report
from mostlyai.qa._sampling import pull_data_for_embeddings, calculate_embeddings
from mostlyai.qa._common import (
    ProgressCallback,
    PrerequisiteNotMetError,
    check_min_sample_size,
    check_statistics_prerequisite,
    determine_data_size,
    REPORT_CREDITS,
    ProgressCallbackWrapper,
)
from mostlyai.qa._filesystem import Statistics, TemporaryWorkspace

_LOG = logging.getLogger(__name__)


def report_from_statistics(
    *,
    syn_tgt_data: pd.DataFrame,
    syn_ctx_data: pd.DataFrame | None = None,
    statistics_path: str | Path | None = None,
    ctx_primary_key: str | None = None,
    tgt_context_key: str | None = None,
    report_path: str | Path | None = "data-report.html",
    report_title: str = "Data Report",
    report_subtitle: str = "",
    report_credits: str = REPORT_CREDITS,
    max_sample_size_accuracy: int | None = None,
    max_sample_size_embeddings: int | None = None,
    update_progress: ProgressCallback | None = None,
) -> Path:
    """
    Generate an HTML report based on previously generated statistics and newly provided synthetic data samples.

    Args:
        syn_tgt_data: The synthetic (target) data.
        syn_ctx_data: The synthetic context data.
        statistics_path: The path from where to fetch the statistics files.
        ctx_primary_key: The primary key of the context data.
        tgt_context_key: The context key of the target data.
        report_path: The path to store the HTML report.
        report_title: The title of the report.
        report_subtitle: The subtitle of the report.
        report_credits: The credits of the report.
        max_sample_size_accuracy: The maximum sample size for accuracy calculations.
        max_sample_size_embeddings: The maximum sample size for embedding calculations (similarity & distances)
        update_progress: The progress callback.

    Returns:
        The path to the generated HTML report.
    """

    with (
        TemporaryWorkspace() as workspace,
        ProgressCallbackWrapper(update_progress) as progress,
    ):
        # prepare report_path
        if report_path is None:
            report_path = Path.cwd() / "data-report.html"
        else:
            report_path = Path(report_path)

        statistics = Statistics(path=statistics_path)

        # determine sample size
        syn_sample_size = determine_data_size(syn_tgt_data, syn_ctx_data, ctx_primary_key, tgt_context_key)

        # early exit if prerequisites are not met
        try:
            check_statistics_prerequisite(statistics)
            check_min_sample_size(syn_sample_size, 100, "synthetic")
        except PrerequisiteNotMetError:
            _html_report.store_early_exit_report(report_path)
            return report_path

        meta = statistics.load_meta()

        # ensure synthetic data is structurally compatible with statistics
        if "trn_tgt_columns" in meta:
            syn_tgt_data = syn_tgt_data[meta["trn_tgt_columns"]]
        if "trn_ctx_columns" in meta and meta["trn_ctx_columns"] is not None:
            if syn_ctx_data is None:
                raise ValueError("syn_ctx_data is required for given statistics")
            syn_ctx_data = syn_ctx_data[meta["trn_ctx_columns"]]

        # prepare data
        _LOG.info("sample synthetic data started")
        syn = _sampling.pull_data_for_accuracy(
            df_tgt=syn_tgt_data,
            df_ctx=syn_ctx_data,
            ctx_primary_key=ctx_primary_key,
            tgt_context_key=tgt_context_key,
            max_sample_size=max_sample_size_accuracy,
            # always pull Sequence Length and nxt columns for synthetic data
            # and let downstream functions decide if they are needed
            setup="1:N",
        )
        _LOG.info(f"sample synthetic data finished ({syn.shape=})")
        progress.update(completed=20, total=100)

        # calculate and plot accuracy and correlations
        acc_uni, acc_biv, corr_trn = _report_accuracy_and_correlations_from_statistics(
            syn=syn,
            statistics=statistics,
            workspace=workspace,
        )
        progress.update(completed=30, total=100)

        _LOG.info("calculate embeddings for synthetic")
        syn_embeds = calculate_embeddings(
            strings=pull_data_for_embeddings(
                df_tgt=syn_tgt_data,
                df_ctx=syn_ctx_data,
                ctx_primary_key=ctx_primary_key,
                tgt_context_key=tgt_context_key,
                max_sample_size=max_sample_size_embeddings,
            ),
            progress=progress,
            progress_from=30,
            progress_to=50,
        )

        _LOG.info("report similarity")
        _report_similarity_from_statistics(
            syn_embeds=syn_embeds,
            workspace=workspace,
            statistics=statistics,
        )
        progress.update(completed=50, total=100)

        meta |= {
            "rows_synthetic": syn.shape[0],
            "report_title": report_title,
            "report_subtitle": report_subtitle,
            "report_credits": report_credits,
        }

        # HTML report
        _html_report.store_report(
            report_path=report_path,
            report_type="data_report",
            workspace=workspace,
            metrics=None,
            meta=meta,
            acc_uni=acc_uni,
            acc_biv=acc_biv,
            corr_trn=corr_trn,
        )
        progress.update(completed=100, total=100)
        return report_path


def _report_accuracy_and_correlations_from_statistics(
    *,
    syn: pd.DataFrame,
    statistics: Statistics,
    workspace: TemporaryWorkspace,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    _LOG.info("load original bins")
    bins = statistics.load_bins()
    syn = syn[bins.keys()].copy()

    _LOG.info("calculate synthetic bins")
    syn_bin, _ = _accuracy.bin_data(syn, bins)

    _LOG.info("load univariates and bivariates")
    acc_uni = statistics.load_univariate_accuracies()
    acc_biv = statistics.load_bivariate_accuracies()

    _LOG.info("load numeric KDEs")
    trn_num_kdes = statistics.load_numeric_uni_kdes()

    _LOG.info("load categorical counts")
    trn_cat_uni_cnts = statistics.load_categorical_uni_counts()

    _LOG.info("load bin counts")
    trn_bin_cnts_uni, trn_bin_cnts_biv = statistics.load_bin_counts()

    _LOG.info("load correlations")
    corr_trn = statistics.load_correlations()

    _LOG.info("calculate synthetic correlations")
    corr_syn = _accuracy.calculate_correlations(binned=syn_bin, corr_cols=corr_trn.columns)

    _LOG.info("plot correlations")
    _accuracy.plot_store_correlation_matrices(corr_trn=corr_trn, corr_syn=corr_syn, workspace=workspace)

    _LOG.info("filter columns for plotting")
    syn = syn[acc_uni["column"]]
    acc_cols = list(set(acc_uni["column"]) | set(acc_biv["col1"]) | set(acc_biv["col2"]))
    syn_bin = syn_bin[acc_cols]

    _LOG.info("calculate numeric KDEs for synthetic")
    syn_num_kdes = _accuracy.calculate_numeric_uni_kdes(df=syn, trn_kdes=trn_num_kdes)

    _LOG.info("calculate categorical counts for synthetic")
    syn_cat_uni_cnts = _accuracy.calculate_categorical_uni_counts(
        df=syn,
        trn_col_counts=trn_cat_uni_cnts,
        hash_rare_values=False,
    )

    _LOG.info("calculate bin counts for synthetic")
    syn_bin_cnts_uni, syn_bin_cnts_biv = _accuracy.calculate_bin_counts(syn_bin)

    _LOG.info("plot univariates")
    _accuracy.plot_store_univariates(
        trn_num_kdes=trn_num_kdes,
        syn_num_kdes=syn_num_kdes,
        trn_cat_cnts=trn_cat_uni_cnts,
        syn_cat_cnts=syn_cat_uni_cnts,
        trn_cnts_uni=trn_bin_cnts_uni,
        syn_cnts_uni=syn_bin_cnts_uni,
        acc_uni=acc_uni,
        workspace=workspace,
        show_accuracy=False,
    )

    _LOG.info("plot bivariates")
    _accuracy.plot_store_bivariates(
        trn_cnts_uni=trn_bin_cnts_uni,
        syn_cnts_uni=syn_bin_cnts_uni,
        trn_cnts_biv=trn_bin_cnts_biv,
        syn_cnts_biv=syn_bin_cnts_biv,
        acc_biv=acc_biv,
        workspace=workspace,
        show_accuracy=False,
    )

    return acc_uni, acc_biv, corr_trn


def _report_similarity_from_statistics(
    *,
    syn_embeds: np.ndarray,
    statistics: Statistics,
    workspace: TemporaryWorkspace,
):
    _LOG.info("load PCA model")
    pca_model = statistics.load_pca_model()
    if pca_model is None:
        _LOG.info("PCA model not found; skipping plotting similarity contours")
        return

    _LOG.info("load training and holdout PCA-projected embeddings")
    trn_pca, hol_pca = statistics.load_trn_hol_pcas()

    _LOG.info("plot and store PCA similarity contours")
    _similarity.plot_store_similarity_contours(
        pca_model=pca_model, trn_pca=trn_pca, hol_pca=hol_pca, syn_embeds=syn_embeds, workspace=workspace
    )
