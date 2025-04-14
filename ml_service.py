from flask import Blueprint, request, jsonify
import joblib
import numpy as np
import traceback

ml = Blueprint("ml", __name__)

# Load the trained model and encoders
model = joblib.load("ingredient_conversion_model.pkl")
encoder_spoon = joblib.load("spoon_encoder.pkl")
encoder_ingredient = joblib.load("ingredient_encoder.pkl")

# 📝 Print available values to build dropdowns
print("✅ Spoon Types:", list(encoder_spoon.classes_))
print("✅ Ingredient Types:", list(encoder_ingredient.classes_))


def predict_conversion(spoon_type, ingredient_type, quantity=1):
    try:
        # ❌ Validation: check if provided values are in encoder
        if spoon_type not in encoder_spoon.classes_:
            print(f"❌ Spoon type '{spoon_type}' not in encoder.")
            return None
        if ingredient_type not in encoder_ingredient.classes_:
            print(f"❌ Ingredient type '{ingredient_type}' not in encoder.")
            return None

        encoded_spoon = encoder_spoon.transform([spoon_type])[0]
        encoded_ingredient = encoder_ingredient.transform([ingredient_type])[0]

        # ✅ Pass 3 features to the model
        input_data = np.array([[encoded_spoon, encoded_ingredient, quantity]])
        predicted_weight = model.predict(input_data)[0]

        return round(predicted_weight, 2)
    except ValueError as ve:
        print("❌ ValueError:", ve)
        return None


@ml.route("/convert", methods=["POST"])
def convert_ingredient():
    try:
        # Support both JSON and form POST
        if request.is_json:
            data = request.get_json()
            spoon = data.get("spoon") or data.get("spoon_type")
            ingredient = data.get("ingredient") or data.get("ingredient_type")
            quantity = float(data.get("quantity", 1))
        else:
            print("📥 Raw request data:", request.form)
            spoon = request.form.get("spoon_type")
            ingredient = request.form.get("ingredient_type")
            quantity = float(request.form.get("quantity", 1))

        print(f"🧪 Inputs — Spoon: {spoon}, Ingredient: {ingredient}, Quantity: {quantity}")

        if not spoon or not ingredient:
            return jsonify({"success": False, "message": "Missing required fields."}), 400

        result = predict_conversion(spoon, ingredient, quantity)

        if result is None:
            return jsonify({"success": False, "message": "Invalid input for conversion."}), 400

        return jsonify({
            "success": True,
            "message": f"{quantity} {spoon} of {ingredient} is approximately {result} grams.",
            "result": result
        })

    except Exception as e:
        print("❌ Error in /ml/convert route:", str(e))
        traceback.print_exc()
        return jsonify({
            "success": False,
            "message": "Conversion failed due to an internal error."
        }), 500
