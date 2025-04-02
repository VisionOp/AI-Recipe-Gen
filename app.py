from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai  # Import Google Gemini AI

app = Flask(__name__)
CORS(app)

# Set up Google Gemini API Key (Replace with your actual API key)
GENAI_API_KEY = "AIzaSyBhvmn7k9NBlTqD9fpvtGFEgD8I0rNswNc"
genai.configure(api_key=GENAI_API_KEY)

@app.route('/generate-recipe', methods=['POST'])
def generate_recipe():
    data = request.get_json()
    ingredients = data.get("ingredients", "")
    dietary_preferences = data.get("dietaryPreferences", "")
    cuisine = data.get("cuisine", "")
    spice_level = data.get("spiceLevel", "")

    # AI Prompt for Free-tier Gemini API
    prompt = (
        f"Create a recipe using these ingredients: {ingredients}. "
        f"Make it {dietary_preferences} and follow {cuisine} style. "
        f"Spice level should be {spice_level}."
    )

    try:
        model = genai.GenerativeModel("gemini-1.5-flash")  # ✅ Free-tier supported model
        response = model.generate_content(prompt)

        recipe = response.text if response and response.text else "Sorry, I couldn't generate a recipe at this moment."
        return jsonify({"recipe": recipe})

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
