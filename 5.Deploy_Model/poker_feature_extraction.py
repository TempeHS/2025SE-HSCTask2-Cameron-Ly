def calculate_hand_strength(ranks, suits):
    ranks_sorted = sorted(ranks)
    unique_ranks = len(set(ranks))
    is_flush = len(set(suits)) == 1

    # Check if it's a straight
    is_straight = (
        len(set(ranks)) == 5 and
        max(ranks) - min(ranks) == 4
    )

    rank_counts = [ranks.count(r) for r in set(ranks)]

    if is_flush and is_straight:
        return 8  # Straight Flush
    elif 4 in rank_counts:
        return 7  # Four of a Kind
    elif sorted(rank_counts) == [2, 3]:
        return 6  # Full House
    elif is_flush:
        return 5  # Flush
    elif is_straight:
        return 4  # Straight
    elif 3 in rank_counts:
        return 3  # Three of a Kind
    elif rank_counts.count(2) == 2:
        return 2  # Two Pair
    elif 2 in rank_counts:
        return 1  # One Pair
    else:
        return 0  # High Card


def calculate_max_rank_frequency(ranks):
    return max([ranks.count(r) for r in ranks])

def calculate_unique_ranks(ranks):
    return len(set(ranks))

def calculate_unique_suits(suits):
    return len(set(suits))
