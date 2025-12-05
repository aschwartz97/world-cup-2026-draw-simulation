"""
Configuration file for FIFA World Cup 2026 Draw Simulator
Contains all constants and parameters used throughout the simulation
"""

# ============================================
# DRAW PARAMETERS
# ============================================

NUM_GROUPS = 12
TEAMS_PER_GROUP = 4
NUM_POTS = 4
TEAMS_PER_POT = 12

# Group names
GROUPS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L']

# ============================================
# CONFEDERATION RESTRICTIONS
# ============================================

MAX_UEFA_PER_GROUP = 2
MAX_OTHER_CONF_PER_GROUP = 1

# ============================================
# FIXED HOST COUNTRIES
# ============================================

FIXED_HOSTS = {
    'Mexico': 'A',
    'Canada': 'B',
    'United States': 'D'
}

# ============================================
# SIMULATION PARAMETERS
# ============================================

NUM_SIMULATIONS = 100000
MAX_ATTEMPTS_PER_SIMULATION = 1000

# Random seed for reproducibility (set to None for true randomness)
RANDOM_SEED = 42

# Progress reporting
SHOW_PROGRESS_EVERY = 10000

# ============================================
# FILE PATHS
# ============================================

# Input files
DATA_DIR = 'data'
POTS_FILE = f'{DATA_DIR}/bombos.csv'
CONFEDERATIONS_FILE = f'{DATA_DIR}/confederaciones.csv'

# Output files
OUTPUT_DIR = 'output'
RESULTS_FILE = f'{OUTPUT_DIR}/resultados_completos.csv'
ANALYSIS_FILE = f'{OUTPUT_DIR}/analisis_estadistico.csv'
TOP_COMBINATIONS_FILE = f'{OUTPUT_DIR}/top_100_combinaciones.csv'

# ============================================
# ANALYSIS PARAMETERS
# ============================================

# Target team for focused analysis
TARGET_TEAM = 'Argentina'

# Number of top results to show in analysis
TOP_N_COMBINATIONS = 100
TOP_N_TEAMS_PER_POT = 10

# ============================================
# DISPLAY SETTINGS
# ============================================

# Decimal places for probability display
PROBABILITY_DECIMALS = 4
PERCENTAGE_DECIMALS = 2