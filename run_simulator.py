"""
Main script to run the FIFA World Cup 2026 Draw Simulation

This script orchestrates the entire simulation process:
1. Load and validate data
2. Run mass simulation
3. Analyze results
4. Export to CSV files

Usage:
    python run_simulation.py
"""

import sys
import random
import numpy as np
from datetime import datetime

# Import modules from code package
from code.config import RANDOM_SEED
from code.data_loader import load_and_validate_all
from code.simulator import run_mass_simulation
from code.analyzer import generate_analysis_report
from code.utils import export_results_to_csv, print_quick_summary


def main():
    """
    Main execution function
    """
    print("=" * 70)
    print("⚽ FIFA WORLD CUP 2026 - DRAW SIMULATOR")
    print("=" * 70)
    print(f"Execution start: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)

    # Set random seed for reproducibility
    if RANDOM_SEED is not None:
        random.seed(RANDOM_SEED)
        np.random.seed(RANDOM_SEED)
        print(f"\n🎲 Random seed set to: {RANDOM_SEED} (for reproducibility)")
    else:
        print(f"\n🎲 Random seed: None (true randomness)")

    try:
        # ============================================
        # STEP 1: Load and validate data
        # ============================================
        print("\n" + "=" * 70)
        print("STEP 1: LOADING DATA")
        print("=" * 70)

        df_pots, df_confederations, conf_dict, pot_dict = load_and_validate_all()

        # ============================================
        # STEP 2: Run mass simulation
        # ============================================
        print("\n" + "=" * 70)
        print("STEP 2: RUNNING SIMULATION")
        print("=" * 70)

        simulation_results = run_mass_simulation(
            df_pots=df_pots,
            conf_dict=conf_dict,
            pot_dict=pot_dict,
            show_progress=True
        )

        # ============================================
        # STEP 3: Analyze results
        # ============================================
        print("\n" + "=" * 70)
        print("STEP 3: ANALYZING RESULTS")
        print("=" * 70)

        analysis_report = generate_analysis_report(
            simulation_results=simulation_results,
            df_pots=df_pots
        )

        # ============================================
        # STEP 4: Export results
        # ============================================
        print("\n" + "=" * 70)
        print("STEP 4: EXPORTING RESULTS")
        print("=" * 70)

        export_results_to_csv(analysis_report, simulation_results)

        # ============================================
        # STEP 5: Print quick summary
        # ============================================
        print_quick_summary(analysis_report)

        # ============================================
        # Completion
        # ============================================
        print("=" * 70)
        print("✅ SIMULATION COMPLETED SUCCESSFULLY!")
        print("=" * 70)
        print(f"Execution end: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("\n📂 Check the 'output/' folder for detailed results")
        print("=" * 70)

        return 0

    except KeyboardInterrupt:
        print("\n\n⚠️ Simulation interrupted by user")
        return 1

    except Exception as e:
        print(f"\n\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)