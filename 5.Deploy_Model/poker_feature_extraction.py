# Mapping for card ranks (cards like Ace, King, etc., are mapped to numbers)
card_mapping = {
    '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14
}

# Mapping for suits (e.g., 'Hearts', 'Diamonds', 'Clubs', 'Spades')
suit_mapping = {
    'Hearts': 'H', 'Diamonds': 'D', 'Clubs': 'C', 'Spades': 'S'
}

def calculate_hand_strength(ranks, suits):
    """
    Function to calculate hand strength based on hand type (e.g., High Card, One Pair, etc.)
    This is a simplified version to calculate the hand strength.
    """
    ranks_sorted = sorted(ranks)
    unique_ranks = len(set(ranks))
    is_flush = len(set(suits)) == 1  # Check if all cards are of the same suit
    is_straight = ranks_sorted == list(range(ranks_sorted[0], ranks_sorted[0] + 5))  # Check for a straight

    # Hand strength classification based on combination of flush, straight, and rank frequency
    if is_flush and is_straight:
        return 8  # Straight Flush
    elif len(set(ranks)) == 2:
        return 7  # Four of a Kind or Full House
    elif is_flush:
        return 5  # Flush
    elif is_straight:
        return 4  # Straight
    elif unique_ranks == 3:
        return 3  # Three of a Kind
    elif unique_ranks == 4:
        return 2  # Two Pair
    elif unique_ranks == 5:
        return 1  # One Pair
    else:
        return 0  # High Card

def calculate_max_rank_frequency(ranks):
    """
    Function to calculate the maximum frequency of any rank in the hand.
    """
    rank_counts = {rank: ranks.count(rank) for rank in set(ranks)}
    max_frequency = max(rank_counts.values())
    return max_frequency

def calculate_unique_ranks(ranks):
    """
    Function to calculate the number of unique ranks in the hand.
    """
    return len(set(ranks))

def calculate_unique_suits(suits):
    """
    Function to calculate the number of unique suits in the hand.
    """
    return len(set(suits))

