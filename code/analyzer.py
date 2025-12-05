"""
Analysis module
Statistical analysis and insights from simulation results
"""

import pandas as pd
import numpy as np
from collections import Counter
from .config import *


def create_results_dataframe(combinations_counter, successful_sims, target_team=TARGET_TEAM):
    """
    Convert combinations counter to a sorted DataFrame with probabilities.

    Args:
        combinations_counter: Dictionary with combination frequencies
        successful_sims: Number of successful simulations
        target_team: Name of the target team

    Returns:
        pd.DataFrame: Sorted results with probabilities
    """
    results_list = []

    for combination, frequency in combinations_counter.items():
        pot2_team, pot3_team, pot4_team = combination
        probability = (frequency / successful_sims) * 100

        results_list.append({
            'Pot 1': target_team,
            'Pot 2': pot2_team,
            'Pot 3': pot3_team,
            'Pot 4': pot4_team,
            'Frequency': frequency,
            'Probability (%)': probability
        })

    # Create DataFrame
    df_results = pd.DataFrame(results_list)

    # Sort by probability (descending)
    df_results = df_results.sort_values('Probability (%)', ascending=False).reset_index(drop=True)

    # Round probabilities
    df_results['Probability (%)'] = df_results['Probability (%)'].round(PROBABILITY_DECIMALS)

    return df_results


def analyze_by_pot(df_results, successful_sims):
    """
    Analyze most frequent teams by pot.

    Args:
        df_results: DataFrame with all combinations
        successful_sims: Number of successful simulations

    Returns:
        dict: {pot_name: DataFrame with team frequencies and probabilities}
    """
    analysis_by_pot = {}

    for pot_col in ['Pot 2', 'Pot 3', 'Pot 4']:
        # Count frequencies by team
        team_frequencies = df_results.groupby(pot_col)['Frequency'].sum().sort_values(ascending=False)

        # Calculate probabilities
        team_probabilities = (team_frequencies / successful_sims * 100).round(PERCENTAGE_DECIMALS)

        # Create DataFrame
        pot_analysis = pd.DataFrame({
            'Team': team_frequencies.index,
            'Frequency': team_frequencies.values,
            'Probability (%)': team_probabilities.values
        }).reset_index(drop=True)

        analysis_by_pot[pot_col] = pot_analysis

    return analysis_by_pot


def calculate_concentration_metrics(df_results):
    """
    Calculate metrics to understand result concentration/randomness.

    Args:
        df_results: DataFrame with all combinations

    Returns:
        dict: Dictionary with concentration metrics
    """
    total_combinations = len(df_results)

    # Top N probabilities
    prob_top_1 = df_results['Probability (%)'].iloc[0] if len(df_results) > 0 else 0
    prob_top_10 = df_results.head(10)['Probability (%)'].sum()
    prob_top_20 = df_results.head(20)['Probability (%)'].sum()
    prob_top_50 = df_results.head(50)['Probability (%)'].sum()
    prob_top_100 = df_results.head(100)['Probability (%)'].sum()

    # Uniform probability (theoretical)
    uniform_prob = 100 / total_combinations if total_combinations > 0 else 0

    # Gini coefficient (concentration measure)
    probabilities = df_results['Probability (%)'].sort_values().values
    n = len(probabilities)
    if n > 0 and probabilities.sum() > 0:
        gini_index = (2 * np.sum((np.arange(1, n + 1)) * probabilities)) / (n * np.sum(probabilities)) - (n + 1) / n
    else:
        gini_index = 0

    return {
        'total_combinations': total_combinations,
        'prob_top_1': prob_top_1,
        'prob_top_10': prob_top_10,
        'prob_top_20': prob_top_20,
        'prob_top_50': prob_top_50,
        'prob_top_100': prob_top_100,
        'uniform_prob': uniform_prob,
        'gini_index': gini_index
    }


def print_analysis_summary(df_results, analysis_by_pot, concentration_metrics,
                           successful_sims, target_team=TARGET_TEAM):
    """
    Print comprehensive analysis summary to console.

    Args:
        df_results: DataFrame with all combinations
        analysis_by_pot: Dictionary with pot-wise analysis
        concentration_metrics: Dictionary with concentration metrics
        successful_sims: Number of successful simulations
        target_team: Name of target team
    """
    print("=" * 70)
    print("📊 STATISTICAL ANALYSIS")
    print("=" * 70)

    # Concentration metrics
    print("\n🎲 1. RANDOMNESS AND PREDICTABILITY METRICS")
    print("-" * 70)
    print(f"\n📈 Concentration metrics:")
    print(f"   • Highest probability (Top 1): {concentration_metrics['prob_top_1']:.4f}%")
    print(f"   • Cumulative probability Top 10: {concentration_metrics['prob_top_10']:.2f}%")
    print(f"   • Cumulative probability Top 20: {concentration_metrics['prob_top_20']:.2f}%")
    print(f"   • Cumulative probability Top 50: {concentration_metrics['prob_top_50']:.2f}%")
    print(f"   • Cumulative probability Top 100: {concentration_metrics['prob_top_100']:.2f}%")
    print(f"\n   • Total possible combinations: {concentration_metrics['total_combinations']:,}")
    print(f"   • Theoretical uniform probability: {concentration_metrics['uniform_prob']:.4f}%")
    print(f"   • Gini index: {concentration_metrics['gini_index']:.4f} (0=uniform, 1=concentrated)")

    # Interpretation
    prob_top_20 = concentration_metrics['prob_top_20']
    print(f"\n💡 INTERPRETATION:")
    if prob_top_20 < 10:
        print(f"   ⚠️ HIGH RANDOMNESS: Top 20 only accounts for {prob_top_20:.2f}% of probability.")
        print(f"   → Restrictions create a very wide possibility space.")
        print(f"   → Difficult to predict the actual draw with certainty.")
    elif prob_top_20 < 20:
        print(f"   📊 MODERATE RANDOMNESS: Top 20 accounts for {prob_top_20:.2f}% of probability.")
        print(f"   → Some concentration in specific scenarios.")
        print(f"   → Most frequent teams have statistical relevance.")
    else:
        print(f"   🎯 LOW RANDOMNESS: Top 20 accounts for {prob_top_20:.2f}% of probability.")
        print(f"   → Strong concentration in certain scenarios.")
        print(f"   → Results are quite predictive.")

    # Most frequent teams by pot
    print(f"\n\n🥇 2. MOST FREQUENT TEAMS BY POT (TOP 10)")
    print("-" * 70)

    for pot_name, pot_analysis in analysis_by_pot.items():
        print(f"\n{pot_name}:")
        top_10 = pot_analysis.head(TOP_N_TEAMS_PER_POT)
        for i, row in top_10.iterrows():
            print(f"   {i + 1:2d}. {row['Team']:40s} {row['Probability (%)']:6.2f}%")

    # Top combinations
    print(f"\n\n🏆 3. TOP {min(10, len(df_results))} MOST LIKELY COMBINATIONS FOR {target_team.upper()}")
    print("=" * 70)

    top_combinations = df_results.head(10)
    for idx, row in top_combinations.iterrows():
        print(f"\n#{idx + 1}")
        print(f"   {target_team}'s Group:")
        print(f"      1. {row['Pot 1']}")
        print(f"      2. {row['Pot 2']}")
        print(f"      3. {row['Pot 3']}")
        print(f"      4. {row['Pot 4']}")
        print(f"   📊 Probability: {row['Probability (%)']:.4f}%  |  Frequency: {row['Frequency']:,}")

    print(f"\n{'=' * 70}\n")


def analyze_top_combinations_patterns(df_results, top_n=50):
    """
    Analyze patterns in top N combinations.

    Args:
        df_results: DataFrame with all combinations
        top_n: Number of top combinations to analyze

    Returns:
        dict: Dictionary with pattern analysis
    """
    top_combinations = df_results.head(top_n)

    patterns = {}

    for pot_col in ['Pot 2', 'Pot 3', 'Pot 4']:
        team_counts = top_combinations[pot_col].value_counts()
        patterns[pot_col] = team_counts

    return patterns


def generate_analysis_report(simulation_results, df_pots, target_team=TARGET_TEAM):
    """
    Generate complete analysis report from simulation results.

    Args:
        simulation_results: Dictionary returned by run_mass_simulation()
        df_pots: DataFrame with team-pot mapping
        target_team: Name of target team

    Returns:
        dict: Complete analysis with all DataFrames and metrics
    """
    print("\n📈 Generating analysis report...\n")

    # Extract data from simulation results
    combinations_counter = simulation_results['combinations']
    successful_sims = simulation_results['successful']

    # Create results DataFrame
    df_results = create_results_dataframe(combinations_counter, successful_sims, target_team)

    # Analyze by pot
    analysis_by_pot = analyze_by_pot(df_results, successful_sims)

    # Calculate concentration metrics
    concentration_metrics = calculate_concentration_metrics(df_results)

    # Analyze top combination patterns
    top_patterns = analyze_top_combinations_patterns(df_results, top_n=50)

    # Print summary
    print_analysis_summary(df_results, analysis_by_pot, concentration_metrics,
                           successful_sims, target_team)

    return {
        'df_results': df_results,
        'analysis_by_pot': analysis_by_pot,
        'concentration_metrics': concentration_metrics,
        'top_patterns': top_patterns,
        'successful_sims': successful_sims
    }