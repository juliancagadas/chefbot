"""
chef_bot.py

This file defines the ChefBot class.

Job of this class (single responsibility):
    - Own one instance of each helper class (NLPProcessor,
      RecipeDatabase, ResponseGenerator).
    - Take one message from the user and coordinate those helpers to
      produce one reply. This is the "brain" that connects everything.

This is also the class that both the terminal version AND the
Tkinter GUI version import and use -- neither interface needs to know
HOW ChefBot thinks, only that it can call process_message(text) and
get a string back. That separation is one of the big benefits of OOP:
you could swap out the GUI for a web app later, and ChefBot itself
would not need to change at all.
"""

from nlp_processor import NLPProcessor
from recipe_database import RecipeDatabase
from response_generator import ResponseGenerator


class ChefBot:
    """Coordinates the NLP pipeline and produces ChefBot's replies."""

    def __init__(self):
        self.nlp = NLPProcessor()
        self.db = RecipeDatabase()
        self.responder = ResponseGenerator()
        self.is_running = True
        self.pending_dish = None

        # Stores the dish when ChefBot is waiting for a recipe variant.
        # Example: "adobo"
        self.pending_dish = None

    def process_message(self, user_input):
        cleaned_text = self.nlp.clean_text(user_input)
        tokens = self.nlp.tokenize(cleaned_text)
        intent = self.nlp.detect_intent(cleaned_text, tokens)

        # Goodbye
        if intent == "goodbye":
            self.is_running = False
            self.pending_dish = None
            return self.responder.goodbye()

        # Check if ChefBot is waiting for a recipe variant
        if self.pending_dish:
            variants = self.db.get_variants(self.pending_dish)

            variant = self.nlp.extract_variant(
                cleaned_text,
                variants
            )

            if variant:
                recipe = self.db.get_variant_recipe(
                    self.pending_dish,
                    variant
                )

                dish_name = f"{variant} {self.pending_dish}"

                self.pending_dish = None

                return self.responder.recipe_instructions(
                    dish_name,
                    recipe["steps"]
                )

            return self.responder.variant_not_found(
                self.pending_dish,
                variants
            )

        # Greeting
        if intent == "greeting":
            return self.responder.greeting()

        # Ingredient substitution
        if intent == "ingredient_substitution":
            ingredient = self.nlp.extract_ingredient(
                cleaned_text,
                self.db.get_all_ingredient_names()
            )

            if ingredient and self.db.has_substitution(ingredient):
                alternatives = self.db.get_substitution(ingredient)

                return self.responder.substitution(
                    ingredient,
                    alternatives
                )

            return self.responder.substitution_not_found(
                ingredient or "that ingredient"
            )

        # Ingredient lookup
        if intent == "ingredient_lookup":
            dish = self.nlp.extract_dish(
                cleaned_text,
                self.db.get_all_dish_names()
            )

            if dish and self.db.has_recipe(dish):

                if self.db.has_variants(dish):
                    variants = self.db.get_variants(dish)

                    self.pending_dish = dish

                    return self.responder.variant_question(
                        dish,
                        variants
                    )

                ingredients = self.db.get_ingredients(dish)

                return self.responder.ingredient_lookup(
                    dish,
                    ingredients
                )

            return self.responder.dish_not_found()

        # Recipe instructions
        if intent == "recipe_instructions":
            dish = self.nlp.extract_dish(
                cleaned_text,
                self.db.get_all_dish_names()
            )

            if dish and self.db.has_recipe(dish):

                if self.db.has_variants(dish):
                    variants = self.db.get_variants(dish)

                    self.pending_dish = dish

                    return self.responder.variant_question(
                        dish,
                        variants
                    )

                steps = self.db.get_steps(dish)

                return self.responder.recipe_instructions(
                    dish,
                    steps
                )

            return self.responder.dish_not_found()

        # Slang
        if intent == "slang_response":
            slang_word = self.nlp.extract_slang(
                cleaned_text,
                tokens
            )

            return self.responder.slang(slang_word)

        # Cooking conversation
        if intent == "cooking_conversation":
            matched_phrase = self.nlp.match_conversation_phrase(
                cleaned_text
            )

            return self.responder.conversation(
                matched_phrase,
                self.nlp.CONVERSATION_PHRASES
            )

        # Fallback
        return self.responder.unknown()

    def run_cli(self):
        """Run ChefBot as a simple terminal chatbot (no GUI)."""
        print("ChefBot: Yo! 👨‍🍳 What's cooking today? (type 'bye' to exit)")
        while self.is_running:
            user_input = input("You: ")
            reply = self.process_message(user_input)
            print(f"ChefBot: {reply}")


if __name__ == "__main__":
    # Running this file directly starts the terminal version.
    ChefBot().run_cli()
