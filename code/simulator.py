"""
Draw simulation module
Contains the core logic for simulating FIFA World Cup 2026 draws
"""

import random
from collections import defaultdict
from .config import *


def can_team_go_to_group(team, group, groups_formed, conf_dict):
    """
    Check if a team can be assigned to a group based on confederation restrictions.

    Args:
        team: Team name
        group: Group letter ('A', 'B', etc.)
        groups_formed: Dictionary with current group formations
        conf_dict: Dictionary mapping teams to their confederation(s)

    Returns:
        bool: True if team can go to the group, False otherwise
    """
    # Get team's confederation(s) (can be a list for playoff teams)
    team_confederations = conf_dict.get(team, [])

    if not team_confederations:
        return True  # If not in dict, allow (shouldn't happen)

    # Get teams already in the group
    teams_in_group = groups_formed.get(group, [])

    # Count confederations currently in the group
    conf_counter = defaultdict(int)
    for existing_team in teams_in_group:
        existing_confs = conf_dict.get(existing_team, [])
        for conf in existing_confs:
            conf_counter[conf] += 1

    # Check each confederation of the team
    for conf in team_confederations:
        if conf == 'UEFA':
            # UEFA can have maximum 2 teams per group
            if conf_counter[conf] >= MAX_UEFA_PER_GROUP:
                return False
        else:
            # Other confederations: maximum 1 team per group
            if conf_counter[conf] >= MAX_OTHER_CONF_PER_GROUP:
                return False

    return True


def get_available_groups_for_team(team, pot_name, groups_formed, groups_filled_by_pot, conf_dict):
    """
    Get list of groups where a team can be assigned.

    Args:
        team: Team name
        pot_name: Pot name ('Pot 1', 'Pot 2', etc.)
        groups_formed: Dictionary with current group formations
        groups_filled_by_pot: Dictionary tracking which groups are filled for each pot
        conf_dict: Dictionary mapping teams to confederations

    Returns:
        list: Available group letters
    """
    available_groups = []

    for group in GROUPS:
        # Skip if group already has a team from this pot
        if group in groups_filled_by_pot.get(pot_name, set()):
            continue

        # Check confederation restrictions
        if can_team_go_to_group(team, group, groups_formed, conf_dict):
            available_groups.append(group)

    return available_groups


def simulate_single_draw(df_pots, conf_dict, pot_dict, max_attempts=MAX_ATTEMPTS_PER_SIMULATION):
    """
    Simulate a single complete draw.

    Args:
        df_pots: DataFrame with team-pot mapping
        conf_dict: Dictionary with team confederations
        pot_dict: Dictionary with teams organized by pot
        max_attempts: Maximum attempts before restarting

    Returns:
        dict: Groups formed {group: [team1, team2, team3, team4]}, or None if failed
    """
    for attempt in range(max_attempts):
        # Initialize empty groups
        groups_formed = {group: [] for group in GROUPS}

        # Track which groups are filled for each pot
        groups_filled_by_pot = {
            'Pot 1': set(),
            'Pot 2': set(),
            'Pot 3': set(),
            'Pot 4': set()
        }

        # ============================================
        # PHASE 1: Draw Pot 1 (Seeded teams)
        # ============================================

        # First, assign fixed hosts
        pot1_teams = pot_dict['Pot 1'].copy()

        for host, fixed_group in FIXED_HOSTS.items():
            if host in pot1_teams:
                groups_formed[fixed_group].append(host)
                groups_filled_by_pot['Pot 1'].add(fixed_group)
                pot1_teams.remove(host)

        # Shuffle remaining Pot 1 teams
        random.shuffle(pot1_teams)

        # Assign remaining Pot 1 teams
        for team in pot1_teams:
            available = get_available_groups_for_team(
                team, 'Pot 1', groups_formed, groups_filled_by_pot, conf_dict
            )

            if not available:
                break  # Restart draw

            assigned_group = random.choice(available)
            groups_formed[assigned_group].append(team)
            groups_filled_by_pot['Pot 1'].add(assigned_group)
        else:
            # Pot 1 completed successfully, continue with other pots
            draw_successful = True

            # ============================================
            # PHASES 2, 3, 4: Draw Pots 4, 3, 2
            # ============================================

            for pot_name in ['Pot 4', 'Pot 3', 'Pot 2']:
                pot_teams = pot_dict[pot_name].copy()
                random.shuffle(pot_teams)

                for team in pot_teams:
                    available = get_available_groups_for_team(
                        team, pot_name, groups_formed, groups_filled_by_pot, conf_dict
                    )

                    if not available:
                        draw_successful = False
                        break  # Restart entire draw

                    assigned_group = random.choice(available)
                    groups_formed[assigned_group].append(team)
                    groups_filled_by_pot[pot_name].add(assigned_group)

                if not draw_successful:
                    break  # Restart entire draw

            # If all pots completed successfully, return result
            if draw_successful:
                return groups_formed

    # If reached here, couldn't complete draw in max_attempts
    return None


def run_mass_simulation(df_pots, conf_dict, pot_dict, num_simulations=NUM_SIMULATIONS,
                        target_team=TARGET_TEAM, show_progress=True):
    """
    Run multiple draw simulations and collect statistics.

    Args:
        df_pots: DataFrame with team-pot mapping
        conf_dict: Dictionary with team confederations
        pot_dict: Dictionary with teams organized by pot
        num_simulations: Number of simulations to run
        target_team: Team to focus analysis on (default: Argentina)
        show_progress: Whether to show progress updates

    Returns:
        dict: {
            'combinations': defaultdict with combination frequencies,
            'successful': number of successful simulations,
            'failed': number of failed simulations
        }
    """
    import time
    from datetime import datetime

    if show_progress:
        print("🚀 MASS SIMULATION - FIFA WORLD CUP 2026 DRAW")
        print("=" * 70)
        print(f"Start time: {datetime.now().strftime('%H:%M:%S')}")
        print("=" * 70)
        print(f"\n⚙️ Configuration:")
        print(f"   • Number of simulations: {num_simulations:,}")
        print(f"   • Target team: {target_team}")
        print(f"\n🎲 Running simulations...\n")

    # Dictionary to count combinations for target team
    # Key: (pot2_team, pot3_team, pot4_team)
    # Value: frequency count
    combinations_counter = defaultdict(int)

    successful_sims = 0
    failed_sims = 0

    start_time = time.time()

    for i in range(1, num_simulations + 1):
        # Show progress
        if show_progress and i % SHOW_PROGRESS_EVERY == 0:
            elapsed = time.time() - start_time
            speed = i / elapsed
            remaining = (num_simulations - i) / speed

            print(f"   Progress: {i:,}/{num_simulations:,} ({i / num_simulations * 100:.1f}%) | "
                  f"Speed: {speed:.0f} sim/sec | "
                  f"Time remaining: {remaining:.0f}s")

        # Run one simulation
        result = simulate_single_draw(df_pots, conf_dict, pot_dict)

        if result:
            successful_sims += 1

            # Find target team's group
            for group, teams in result.items():
                if target_team in teams:
                    # Identify teams from each pot
                    pot1_team = None
                    pot2_team = None
                    pot3_team = None
                    pot4_team = None

                    for team in teams:
                        pot = df_pots[df_pots['Team'] == team]['Pot'].values[0]

                        if pot == 'Pot 1':
                            pot1_team = team
                        elif pot == 'Pot 2':
                            pot2_team = team
                        elif pot == 'Pot 3':
                            pot3_team = team
                        elif pot == 'Pot 4':
                            pot4_team = team

                    # Create combination key (excluding Pot 1 since it's always the target team)
                    combination = (pot2_team, pot3_team, pot4_team)
                    combinations_counter[combination] += 1

                    break
        else:
            failed_sims += 1

    total_time = time.time() - start_time

    if show_progress:
        print(f"\n{'=' * 70}")
        print("✅ SIMULATION COMPLETED")
        print(f"{'=' * 70}")
        print(f"Total time: {total_time:.2f} seconds")
        print(f"Average speed: {num_simulations / total_time:.0f} simulations/second")
        print(f"\n📊 Statistics:")
        print(f"   • Successful simulations: {successful_sims:,} ({successful_sims / num_simulations * 100:.2f}%)")
        print(f"   • Failed simulations: {failed_sims:,} ({failed_sims / num_simulations * 100:.2f}%)")
        print(f"   • Unique combinations found: {len(combinations_counter):,}")
        print(f"{'=' * 70}\n")

    return {
        'combinations': combinations_counter,
        'successful': successful_sims,
        'failed': failed_sims,
        'total_time': total_time
    }