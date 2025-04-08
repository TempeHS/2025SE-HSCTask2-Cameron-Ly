import pickle
import numpy as np
from flask import Flask, render_template, request

app = Flask(__name__)

# Load the trained model
try:
    with open('trained_model.pkl', 'rb') as f:
        model = pickle.load(f)
    print("Model loaded successfully")
except Exception as e:
    print(f"Error loading model: {e}")
    model = None

POKER_ACTIONS = ['Fold', 'Check', 'Call', 'Raise', 'All-in']

@app.route('/', methods=['GET', 'POST'])
def index():
    prediction = None
    error_message = None
    card_inputs = [''] * 5
    cards_display = [''] * 5

    if request.method == 'POST':
        try:
            if not model:
                raise ValueError("Model not loaded")

            cards = []
            for i in range(5):
                card = request.form.get(f'card{i+1}', '').strip()
                if not card:
                    raise ValueError(f"Card {i+1} is required")
                cards.append(card)
                card_inputs[i] = card

            # Extract ranks, suits and display format
            ranks, suits, display_cards = get_card_details(cards)
            cards_display = display_cards

            # Extract the 4 features expected by the model
            features = calculate_features(ranks, suits)

            # Get predictions from regression model
            raw_prediction = model.predict(features)
            prediction_probs = np.array(raw_prediction[0])
            prediction_probs = prediction_probs / prediction_probs.sum()

            # Pair with labels and sort
            prediction = list(zip(POKER_ACTIONS, prediction_probs))
            prediction.sort(key=lambda x: x[1], reverse=True)

        except Exception as e:
            error_message = f"Error: {str(e)}"

    return render_template(
        'predict.html',
        prediction=prediction,
        error=error_message,
        card_inputs=card_inputs,
        cards_display=cards_display
    )


def get_card_details(cards):
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

    ranks = []
    suits = []
    display_cards = []

    for card in cards:
        card_upper = card.upper().replace('OF', '').strip()
        parts = [p for p in card_upper.split() if p]

        if len(parts) < 1:
            raise ValueError("Invalid card format")

        rank = parts[0]
        if rank == '1' and len(parts) > 1 and parts[1] == '0':
            rank = '10'
            parts.pop(1)
        if rank not in rank_map:
            raise ValueError(f"Invalid rank: {rank}")

        suit = parts[-1] if len(parts) > 1 else ''
        if suit not in suit_map:
            raise ValueError(f"Invalid suit: {suit}")

        ranks.append(rank_map[rank])
        suits.append(suit_map[suit])
        display_cards.append(f"{rank.upper()}{suit_map[suit]}")

    return ranks, suits, display_cards


def calculate_features(ranks, suits):
    rank_counts = {}
    for r in ranks:
        rank_counts[r] = rank_counts.get(r, 0) + 1

    max_rank_freq = max(rank_counts.values())
    unique_ranks = len(rank_counts)
    unique_suits = len(set(suits))

    if max_rank_freq == 4:
        hand_strength = 0.9
    elif max_rank_freq == 3 and unique_ranks == 2:
        hand_strength = 0.8
    elif unique_suits == 1:
        hand_strength = 0.7
    elif max_rank_freq == 3:
        hand_strength = 0.6
    elif max_rank_freq == 2 and unique_ranks == 3:
        hand_strength = 0.5
    elif max_rank_freq == 2:
        hand_strength = 0.4
    else:
        hand_strength = 0.3

    return np.array([[hand_strength, max_rank_freq, unique_ranks, unique_suits]])


if __name__ == '__main__':
    app.run(debug=True)
