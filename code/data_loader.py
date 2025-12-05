"""
Data loading and validation module
Handles loading data from CSV files and validating its structure
"""

import pandas as pd
from collections import defaultdict, Counter
from .config import *


def load_pots(file_path=POTS_FILE):
    """
    Load teams and their pots from CSV file.

    Args:
        file_path: Path to the pots CSV file

    Returns:
        pd.DataFrame: DataFrame with columns ['Team', 'Pot']
    """
    try:
        df = pd.read_csv(file_path)

        # Validate columns
        required_cols = ['Team', 'Pot']
        if not all(col in df.columns for col in required_cols):
            raise ValueError(f"CSV must contain columns: {required_cols}")

        # Clean whitespace
        df['Team'] = df['Team'].str.strip()
        df['Pot'] = df['Pot'].str.strip()

        print(f"✅ Pots loaded: {len(df)} teams")
        return df

    except FileNotFoundError:
        raise FileNotFoundError(f"❌ File not found: {file_path}")
    except Exception as e:
        raise Exception(f"❌ Error loading pots: {e}")


def load_confederations(file_path=CONFEDERATIONS_FILE):
    """
    Load teams and their confederations from CSV file.

    Args:
        file_path: Path to the confederations CSV file

    Returns:
        pd.DataFrame: DataFrame with columns ['Team', 'Confederation']
    """
    try:
        df = pd.read_csv(file_path)

        # Validate columns
        required_cols = ['Team', 'Confederation']
        if not all(col in df.columns for col in required_cols):
            raise ValueError(f"CSV must contain columns: {required_cols}")

        # Clean whitespace
        df['Team'] = df['Team'].str.strip()
        df['Confederation'] = df['Confederation'].str.strip()

        print(f"✅ Confederations loaded: {len(df)} entries")
        return df

    except FileNotFoundError:
        raise FileNotFoundError(f"❌ File not found: {file_path}")
    except Exception as e:
        raise Exception(f"❌ Error loading confederations: {e}")


def create_confederation_dict(df_confederations):
    """
    Create a dictionary mapping each team to its confederation(s).
    Teams with multiple confederations (playoffs) will have a list.

    Args:
        df_confederations: DataFrame with team-confederation mapping

    Returns:
        dict: {team_name: [confederation(s)]}
    """
    conf_dict = {}
    for team in df_confederations['Team'].unique():
        confederations = df_confederations[
            df_confederations['Team'] == team
            ]['Confederation'].tolist()
        conf_dict[team] = confederations

    return conf_dict


def create_pot_dict(df_pots):
    """
    Create a dictionary organizing teams by pot.

    Args:
        df_pots: DataFrame with team-pot mapping

    Returns:
        dict: {pot_name: [team1, team2, ...]}
    """
    pot_dict = {}
    for pot in df_pots['Pot'].unique():
        teams = df_pots[df_pots['Pot'] == pot]['Team'].tolist()
        pot_dict[pot] = teams

    return pot_dict


def validate_data(df_pots, df_confederations):
    """
    Validate the loaded data for consistency and completeness.

    Args:
        df_pots: DataFrame with pots
        df_confederations: DataFrame with confederations

    Returns:
        bool: True if validation passes, raises exception otherwise
    """
    print("\n" + "=" * 60)
    print("🔍 DATA VALIDATION")
    print("=" * 60)

    # Validate pot distribution
    print(f"\n📊 POTS:")
    print(f"   Total teams: {len(df_pots)}")
    print(f"   Expected: {NUM_POTS * TEAMS_PER_POT} ({NUM_POTS} pots × {TEAMS_PER_POT} teams)")

    pots_count = df_pots['Pot'].value_counts().sort_index()
    print(f"\n   Distribution by pot:")
    for pot, count in pots_count.items():
        status = "✅" if count == TEAMS_PER_POT else "⚠️"
        print(f"   {status} {pot}: {count} teams")

    # Check for duplicate teams in pots (except playoff teams)
    unique_teams_pots = df_pots['Team'].nunique()
    print(f"\n   Unique teams in pots: {unique_teams_pots}")

    # Validate confederations
    print(f"\n📊 CONFEDERATIONS:")
    print(f"   Total entries: {len(df_confederations)}")

    conf_count = df_confederations['Confederation'].value_counts().sort_index()
    print(f"\n   Distribution by confederation:")
    for conf, count in conf_count.items():
        print(f"   • {conf}: {count} teams")

    # Identify teams with multiple confederations (playoffs)
    teams_multi_conf = df_confederations['Team'].value_counts()
    teams_multi_conf = teams_multi_conf[teams_multi_conf > 1]

    if len(teams_multi_conf) > 0:
        print(f"\n   ⚠️ Teams with multiple confederations (playoffs): {len(teams_multi_conf)}")
        for team, count in teams_multi_conf.items():
            confs = df_confederations[
                df_confederations['Team'] == team
                ]['Confederation'].values
            print(f"      • {team}: {' and '.join(confs)}")
    else:
        print("\n   ℹ️ No teams with multiple confederations")

    # Verify all pot teams are in confederations
    print("\n" + "=" * 60)
    print("🔐 INTEGRITY CHECK")
    print("=" * 60)

    teams_pots_set = set(df_pots['Team'].unique())
    teams_conf_set = set(df_confederations['Team'].unique())

    missing_teams = teams_pots_set - teams_conf_set
    if len(missing_teams) > 0:
        print(f"\n⚠️ WARNING: {len(missing_teams)} teams in pots missing from confederations:")
        for team in missing_teams:
            print(f"   • {team}")
        raise ValueError("Data integrity check failed: missing confederations")
    else:
        print("\n✅ All pot teams have confederation data")

    # Verify fixed hosts
    print("\n📍 Fixed hosts verification:")
    for host, group in FIXED_HOSTS.items():
        if host in df_pots['Team'].values:
            pot = df_pots[df_pots['Team'] == host]['Pot'].values[0]
            status = "✅" if pot == 'Pot 1' else "⚠️"
            print(f"   {status} {host}: found in {pot} → Group {group}")
        else:
            print(f"   ❌ {host}: NOT FOUND in pots")
            raise ValueError(f"Fixed host {host} not found in pots data")

    print("\n" + "=" * 60)
    print("✅ Validation completed successfully!")
    print("=" * 60)

    return True


def load_and_validate_all():
    """
    Load and validate all required data files.

    Returns:
        tuple: (df_pots, df_confederations, conf_dict, pot_dict)
    """
    print("📊 Loading data from CSV files...\n")

    # Load data
    df_pots = load_pots()
    df_confederations = load_confederations()

    # Create dictionaries
    conf_dict = create_confederation_dict(df_confederations)
    pot_dict = create_pot_dict(df_pots)

    print(f"\n✅ Dictionaries created:")
    print(f"   • Teams with confederation data: {len(conf_dict)}")
    print(f"   • Pots: {len(pot_dict)}")

    # Validate
    validate_data(df_pots, df_confederations)

    return df_pots, df_confederations, conf_dict, pot_dict