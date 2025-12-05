"""
Utility functions
Helper functions for file I/O and data export
"""

import os
import pandas as pd
from datetime import datetime
from .config import *


def ensure_output_directory():
    """
    Create output directory if it doesn't exist.
    """
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        print(f"✅ Created output directory: {OUTPUT_DIR}")


def export_results_to_csv(analysis_report, simulation_results):
    """
    Export all analysis results to CSV files.

    Args:
        analysis_report: Dictionary with analysis results
        simulation_results: Dictionary with simulation results
    """
    ensure_output_directory()

    print("\n💾 EXPORTING RESULTS TO CSV")
    print("=" * 70)

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

    # 1. Export complete results
    df_results = analysis_report['df_results']
    results_file = f"{OUTPUT_DIR}/resultados_completos_{timestamp}.csv"
    df_results.to_csv(results_file, index=False)
    print(f"✅ Complete results: {results_file}")
    print(f"   • Total combinations: {len(df_results):,}")

    # 2. Export Top 100 combinations
    top_100_file = f"{OUTPUT_DIR}/top_100_combinaciones_{timestamp}.csv"
    df_results.head(TOP_N_COMBINATIONS).to_csv(top_100_file, index=False)
    print(f"✅ Top 100 combinations: {top_100_file}")

    # 3. Export analysis by pot
    analysis_by_pot = analysis_report['analysis_by_pot']

    for pot_name, pot_df in analysis_by_pot.items():
        pot_file = f"{OUTPUT_DIR}/analisis_{pot_name.replace(' ', '_').lower()}_{timestamp}.csv"
        pot_df.to_csv(pot_file, index=False)
        print(f"✅ {pot_name} analysis: {pot_file}")

    # 4. Export summary statistics
    summary_data = {
        'Metric': [
            'Total Simulations',
            'Successful Simulations',
            'Failed Simulations',
            'Success Rate (%)',
            'Unique Combinations',
            'Total Time (seconds)',
            'Average Speed (sim/sec)',
            'Highest Probability (%)',
            'Top 10 Cumulative Probability (%)',
            'Top 20 Cumulative Probability (%)',
            'Top 50 Cumulative Probability (%)',
            'Top 100 Cumulative Probability (%)',
            'Gini Index'
        ],
        'Value': [
            NUM_SIMULATIONS,
            simulation_results['successful'],
            simulation_results['failed'],
            round((simulation_results['successful'] / NUM_SIMULATIONS) * 100, 2),
            len(df_results),
            round(simulation_results['total_time'], 2),
            round(NUM_SIMULATIONS / simulation_results['total_time'], 0),
            analysis_report['concentration_metrics']['prob_top_1'],
            analysis_report['concentration_metrics']['prob_top_10'],
            analysis_report['concentration_metrics']['prob_top_20'],
            analysis_report['concentration_metrics']['prob_top_50'],
            analysis_report['concentration_metrics']['prob_top_100'],
            round(analysis_report['concentration_metrics']['gini_index'], 4)
        ]
    }

    df_summary = pd.DataFrame(summary_data)
    summary_file = f"{OUTPUT_DIR}/simulation_summary_{timestamp}.csv"
    df_summary.to_csv(summary_file, index=False)
    print(f"✅ Simulation summary: {summary_file}")

    print(f"\n{'=' * 70}")
    print(f"✅ All results exported successfully!")
    print(f"{'=' * 70}\n")


def print_quick_summary(analysis_report, target_team=TARGET_TEAM):
    """
    Print a quick summary of key findings.

    Args:
        analysis_report: Dictionary with analysis results
        target_team: Name of target team
    """
    df_results = analysis_report['df_results']
    analysis_by_pot = analysis_report['analysis_by_pot']

    print("\n" + "=" * 70)
    print(f"🎯 QUICK SUMMARY - {target_team.upper()}'S GROUP")
    print("=" * 70)

    print("\n📊 Most Likely Opponents:")

    for pot_name in ['Pot 2', 'Pot 3', 'Pot 4']:
        top_team = analysis_by_pot[pot_name].iloc[0]
        print(f"   • {pot_name}: {top_team['Team']} ({top_team['Probability (%)']:.2f}%)")

    print("\n🏆 Most Likely Complete Group:")
    top_group = df_results.iloc[0]
    print(f"   1. {top_group['Pot 1']}")
    print(f"   2. {top_group['Pot 2']}")
    print(f"   3. {top_group['Pot 3']}")
    print(f"   4. {top_group['Pot 4']}")
    print(f"   Probability: {top_group['Probability (%)']:.4f}%")

    print("\n" + "=" * 70 + "\n")


def create_simulation_metadata():
    """
    Create metadata about the simulation run.

    Returns:
        dict: Metadata dictionary
    """
    return {
        'timestamp': datetime.now().isoformat(),
        'num_simulations': NUM_SIMULATIONS,
        'target_team': TARGET_TEAM,
        'random_seed': RANDOM_SEED,
        'num_groups': NUM_GROUPS,
        'teams_per_group': TEAMS_PER_GROUP,
        'max_uefa_per_group': MAX_UEFA_PER_GROUP,
        'max_other_conf_per_group': MAX_OTHER_CONF_PER_GROUP
    }