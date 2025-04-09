# poker_feature_extraction.py

import numpy as np
from collections import Counter

rank_map = {
    '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10,
    'J': 11, 'JACK': 11, 'Q': 12, 'QUEEN': 12, 'K': 13, 'KING': 13,
    'A': 14, 'ACE': 14
}

suit_map = {
    'H': '♥', 'HEARTS': '♥',
    'D': '♦', 'DIAMONDS': '♦',
    'C': '♣', 'CLUBS': '♣',
    'S': '♠', 'SPADES': '♠'
}

def get_card_details(cards):
    """Convert card strings to numerical ranks, suit codes, and display formats"""
    ranks = []
    suits = []
    display_cards = []

    for card in cards:
        card_upper = card.upper().replace('OF', '').strip()
        parts = [p for p in card_upper.split() if p]

        if len(parts) >= 2:
            rank = parts[0]
            suit = parts[-1]
        else:
            raise ValueError(f"Invalid card format: {card}")

        # Handle "10" being split as "1" and "0"
        if rank == '1' and len(parts) > 1 and parts[1] == '0':
            rank = '10'
            suit = parts[2] if len(parts) > 2 else parts[1]

        if rank not in rank_map:
            raise ValueError(f"Invalid rank: {rank}")
        if suit not in suit_map:
            raise ValueError(f"Invalid suit: {suit}")

        ranks.append(rank_map[rank])
        suits.append(suit_map[suit])
        display_cards.append(f"{rank.upper()}{suit_map[suit]}")

    return ranks, suits, display_cards


def calculate_features(ranks, suits):
    """Calculate the 4 features required by the model"""
    rank_counts = Counter(ranks)
    suit_counts = Counter(suits)
    unique_ranks = len(rank_counts)
    unique_suits = len(suit_counts)
    max_rank_freq = max(rank_counts.values())

    sorted_ranks = sorted(set(ranks))
    is_flush = unique_suits == 1
    is_straight = False

    if len(sorted_ranks) == 5:
        if sorted_ranks[-1] - sorted_ranks[0] == 4:
            is_straight = True
        elif sorted_ranks == [2, 3, 4, 5, 14]:  # Ace-low straight
            is_straight = True

    is_royal = sorted_ranks == [10, 11, 12, 13, 14]

    if is_flush and is_royal:
        hand_strength = 1.0
    elif is_flush and is_straight:
        hand_strength = 0.95
    elif max_rank_freq == 4:
        hand_strength = 0.9
    elif max_rank_freq == 3 and unique_ranks == 2:
        hand_strength = 0.85
    elif is_flush:
        hand_strength = 0.8
    elif is_straight:
        hand_strength = 0.75
    elif max_rank_freq == 3:
        hand_strength = 0.6
    elif list(rank_counts.values()).count(2) == 2:
        hand_strength = 0.5
    elif max_rank_freq == 2:
        hand_strength = 0.4
    else:
        hand_strength = 0.3

    return np.array([[hand_strength, max_rank_freq, unique_ranks, unique_suits]])
