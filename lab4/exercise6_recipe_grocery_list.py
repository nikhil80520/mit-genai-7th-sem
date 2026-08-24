"""Exercise 6: Extract recipe ingredients, then scale a grocery list."""
import json
import os

from dotenv import load_dotenv
from groq import Groq

load_dotenv()
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise RuntimeError("GROQ_API_KEY is missing from .env")
client = Groq(api_key=api_key)
MODEL = "openai/gpt-oss-20b"

INGREDIENTS_PROMPT = """Extract recipe servings and ingredients. Return valid JSON only:
{"servings": number or null, "ingredients": [{"item": "...", "quantity": number or null, "unit": "..." or null, "notes": "..." or null}]}. Extract only stated ingredients and quantities; do not estimate."""
GROCERY_PROMPT = """Create a consolidated grocery list for the target number of servings
using only the supplied extracted recipe data. Scale numeric quantities from the
stated original servings. If scaling is impossible because data is missing, keep
the ingredient and clearly mark it 'quantity to confirm'. Return only a Markdown
bullet list grouped under sensible grocery categories. Do not add ingredients."""


def extract_ingredients(recipe_text):
    response = client.chat.completions.create(model=MODEL, temperature=0, max_tokens=800,
        response_format={"type": "json_object"}, messages=[{"role": "system", "content": INGREDIENTS_PROMPT}, {"role": "user", "content": recipe_text}])
    result = json.loads(response.choices[0].message.content)
    if set(result) != {"servings", "ingredients"} or not isinstance(result["ingredients"], list):
        raise ValueError("Ingredient response did not match the required structure.")
    return result


def build_grocery_list(extracted_ingredients, target_servings):
    if target_servings <= 0:
        raise ValueError("target_servings must be positive.")
    payload = {"target_servings": target_servings, "extracted_recipe": extracted_ingredients}
    response = client.chat.completions.create(model=MODEL, temperature=0, max_tokens=600,
        messages=[{"role": "system", "content": GROCERY_PROMPT}, {"role": "user", "content": json.dumps(payload, indent=2)}])
    return response.choices[0].message.content.strip()


if __name__ == "__main__":
    recipe = input("Recipe text: ").strip()
    servings = int(input("Target servings: ").strip())
    if not recipe:
        raise ValueError("Recipe text is required.")
    ingredients = extract_ingredients(recipe)
    print("\nExtracted ingredients:\n" + json.dumps(ingredients, indent=2))
    print("\nScaled grocery list:\n" + build_grocery_list(ingredients, servings))
