import pickle
import numpy as np
from flask import Flask, render_template, request
from poker_feature_extraction import get_card_details, calculate_features

app = Flask(__name__)

# Load model from .pkl
try:
    with open('trained_model.pkl', 'rb') as f:
        model = pickle.load(f)
    print("Model loaded successfully.")
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
                raise ValueError("Prediction model not loaded")

            cards = []
            for i in range(5):
                card = request.form.get(f'card{i+1}', '').strip()
                if not card:
                    raise ValueError(f"Card {i+1} is required")
                cards.append(card)
                card_inputs[i] = card

            ranks, suits, display_cards = get_card_details(cards)
            cards_display = display_cards

            features = calculate_features(ranks, suits)
            prediction_probs = model.predict(features)[0]
            prediction_probs = prediction_probs / prediction_probs.sum()

            prediction = list(zip(POKER_ACTIONS, prediction_probs))
            prediction.sort(key=lambda x: x[1], reverse=True)

        except Exception as e:
            error_message = f"Error: {str(e)}"

    return render_template(
        'index.html',
        prediction=prediction,
        error=error_message,
        card_inputs=card_inputs,
        cards_display=cards_display,
        show_results=prediction is not None
    )

if __name__ == '__main__':
    app.run(debug=True)
