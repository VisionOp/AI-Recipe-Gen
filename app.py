from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai  # Import Google Gemini AI
import os

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests (important for frontend)

# Set up Google Gemini API Key (From Railway Environment Variables)
GENAI_API_KEY = os.getenv("AIzaSyBhvmn7k9NBlTqD9fpvtGFEgD8I0rNswNc")  # Load API Key from Environment Variables
genai.configure(api_key=GENAI_API_KEY)

@app.route('/generate-recipe', methods=['POST'])
def generate_recipe():
    data = request.get_json()
    ingredients = data.get("ingredients", "")
    dietary_preferences = data.get("dietaryPreferences", "")

    prompt = f"Suggest a delicious recipe using: {ingredients}. Dietary preference: {dietary_preferences}."

    try:
        model = genai.GenerativeModel("gemini-1.5-flash")  # Ensure correct model
        response = model.generate_content(prompt)

        if response and hasattr(response, 'text'):
            recipe = response.text
        else:
            recipe = "Sorry, I couldn't generate a recipe at this moment."

        return jsonify({"recipe": recipe})

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
