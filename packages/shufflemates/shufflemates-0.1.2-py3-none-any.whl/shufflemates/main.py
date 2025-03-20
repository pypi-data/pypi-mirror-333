import random
import math
import time
import os


def shuffle_groups(members, group_size, fixed_pairs=None, locked_teams=None):
    """
    Shuffle a list of members and divide them into evenly sized groups,
    while ensuring that fixed pairs are in the same group and locked teams are not changed.

    :param members: List of members to group.
    :param group_size: Desired number of members per group.
    :param fixed_pairs: List of tuples containing members that must be grouped together.
    :param locked_teams: List of tuples containing members that must stay as a separate group.
    :return: List of groups with balanced sizes.
    """
    if fixed_pairs is None:
        fixed_pairs = []
    if locked_teams is None:
        locked_teams = []

    grouped_members = [list(pair) for pair in fixed_pairs]
    locked_groups = [list(team) for team in locked_teams]

    fixed_members = {m for pair in fixed_pairs for m in pair}
    locked_members = {m for team in locked_teams for m in team}

    # Remove fixed and locked members from the list
    remaining_members = [
        m for m in members
        if m not in fixed_members and m not in locked_members]
    random.shuffle(remaining_members)

    # Add locked teams to the grouped members
    for group in grouped_members:
        while len(group) < group_size and remaining_members:
            group.append(remaining_members.pop())

    num_groups = math.ceil(len(members) / group_size)

    # Distribute remaining members into groups
    for _ in range(num_groups - (len(grouped_members) + len(locked_groups))):
        size = group_size
        if len(remaining_members) < size:
            size = len(remaining_members)
        grouped_members.append(remaining_members[:size])
        remaining_members = remaining_members[size:]

    if len(grouped_members) > 1 and len(grouped_members[-1]) < group_size // 2:
        last_group = grouped_members.pop()
        for i, member in enumerate(last_group):
            grouped_members[i % len(grouped_members)].append(member)

    final_groups = locked_groups + grouped_members
    random.shuffle(final_groups)

    return final_groups


def print_shuffle_groups(
    members,
    group_size,
    fixed_pairs=None,
    locked_teams=None,
    num_iterations=12,
    iterations_time=0.5,
):
    """
    Shuffle a list of members and divide them into evenly sized groups,
    while ensuring that fixed pairs are in the same group and locked teams are not changed.
    Print the groups to the console at regular intervals.


    :param members: List of members to group.
    :param
    group_size: Desired number of members per group.
    :param fixed_pairs: List of tuples containing members that must be grouped together.
    :param locked_teams: List of tuples containing members that must stay as a separate group.
    :param num_iterations: Number of times to shuffle and print the groups.
    :param iterations_time: Time to wait between each iteration.
    """
    for i in range(num_iterations):
        os.system("clear")
        groups = shuffle_groups(members, group_size, fixed_pairs, locked_teams)

        for idx, group in enumerate(groups, 1):
            print(f"Group {idx}: {group}")

        time.sleep(iterations_time)
