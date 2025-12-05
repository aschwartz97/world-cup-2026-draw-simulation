"""
FIFA World Cup 2026 Draw Simulator
A Monte Carlo simulation of the World Cup draw with all official restrictions.
"""

__version__ = "1.0.0"
__author__ = "Ariel Schwartz"

# Import main functions for easier access
from .data_loader import load_and_validate_all
from .simulator import run_mass_simulation
from .analyzer import generate_analysis_report
from .utils import export_results_to_csv, print_quick_summary