import pickle
import numpy as np
from flask import Flask, render_template, request
from poker_feature_extraction import calculate_hand_strength, calculate_max_rank_frequency, calculate_unique_ranks, calculate_unique_suits  # Assuming these functions are defined

app = Flask(__name__)

# Load the pre-trained model
with open('trained_model.pkl', 'rb') as f:
    model = pickle.load(f)

@app.route('/', methods=['GET', 'POST'])
def index():
    prediction = None
    if request.method == 'POST':
        # Get card details from user input
        card1 = request.form['card1']
        card2 = request.form['card2']
        card3 = request.form['card3']
        card4 = request.form['card4']
        card5 = request.form['card5']

        # Extract ranks and suits from the cards
        ranks, suits = get_card_details(card1, card2, card3, card4, card5)

        # Calculate features
        hand_strength = calculate_hand_strength(ranks, suits)  # Calculate hand strength (feature 1)
        max_rank_frequency = calculate_max_rank_frequency(ranks)  # Calculate max rank frequency (feature 2)
        unique_ranks = calculate_unique_ranks(ranks)  # Calculate unique ranks (feature 3)
        unique_suits = calculate_unique_suits(suits)  # Calculate unique suits (feature 4)

        # Prepare input for prediction
        features = np.array([[hand_strength, max_rank_frequency, unique_ranks, unique_suits]])

        # Predict action using the model
        prediction = model.predict(features)

    return render_template('index.html', prediction=prediction)

# Function to extract ranks and suits from input cards
def get_card_details(card1, card2, card3, card4, card5):
    card_mapping = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}
    suit_mapping = {'Hearts': 'H', 'Diamonds': 'D', 'Clubs': 'C', 'Spades': 'S'}

    cards = [card1, card2, card3, card4, card5]

    ranks = []
    suits = []

    for card in cards:
        rank, suit = card.split(' of ')  # Extract rank and suit from the input
        ranks.append(card_mapping[rank])
        suits.append(suit_mapping[suit])

    return ranks, suits

if __name__ == '__main__':
    app.run(debug=True)
