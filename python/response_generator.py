"""
response_generator.py

This file defines the ResponseGenerator class.

Job of this class (single responsibility):
    - Take an intent (and any extracted info, like a dish name) and
      turn it into an actual sentence to show the user.
    - Hold all of ChefBot's "personality" text: greetings, goodbyes,
      slang replies, fallback messages, etc.

This is the NLG (Natural Language Generation) part of the pipeline --
though here "generation" just means picking and filling in a
template, not anything AI-driven.
"""

import random


class ResponseGenerator:
    """Builds ChefBot's reply text based on intent + extracted info."""

    def __init__(self):
        # Lists of possible replies. We use lists (not sets) because
        # order/repetition doesn't matter for meaning, but
        # random.choice() needs an indexable sequence.
        self._greetings = [
            "Yo! 👨‍🍳 What's cooking today? Need ingredients, a recipe, or just wanna talk food?",
            "Hey there, chef! What are we making today?",
            "Hi! Ready to get cooking? Ask me about ingredients, steps, or substitutions.",
        ]

        self._goodbyes = [
            "Catch you later, chef! Keep cooking and keep slaying! 👨‍🍳",
            "Bye for now! Come back whenever you need a recipe. 🍳",
        ]

        self._unknown_responses = [
            "That's outside my kitchen for now! 🍳 I can help with ingredients, "
            "cooking instructions, recipes, and food-related conversations.",
            "Hmm, I didn't quite catch that. Try asking me about a recipe, "
            "ingredients, or a substitution!",
        ]

        # Dictionary of slang -> response. A dictionary is the natural
        # fit here: each slang word maps to exactly one canned reply.
        self._slang_responses = {
            "bet": "Bet! Let's get those ingredients ready. 🔥",
            "no cap": "No cap! Glad you're enjoying the cooking journey. 👨‍🍳",
            "cap": "Nah, no cap here -- everything I tell you is straight from the recipe book!",
            "slay": "We love a confident chef! Slay that recipe. 💪",
            "rizz": "Haha, cooking good food is definitely part of the rizz. What are we making?",
            "sus": "Nothing sus going on here, just good honest cooking tips!",
            "mid": "Fair! Let's see what we can improve. Want to try a different recipe?",
            "no joke": "No joke! We're serious about good food around here. 👨‍🍳",
            "for real": "For real! Let's get cooking. 🔥",
            "fr": "FR! Let's make something delicious. 👨‍🍳",
            "that's fire": "That's fire! 🔥 What are we cooking next?",
        }

    # ------------------------------------------------------------------
    # SIMPLE, FIXED-STYLE RESPONSES
    # ------------------------------------------------------------------

    def greeting(self):
        return random.choice(self._greetings)

    def goodbye(self):
        return random.choice(self._goodbyes)

    def unknown(self):
        return random.choice(self._unknown_responses)

    def slang(self, slang_word):
        return self._slang_responses.get(
            slang_word,
            "Haha, I see you! Anyway, what are we cooking today?",
        )

    def conversation(self, matched_phrase, phrase_to_response):
        """
        matched_phrase: the phrase found in the user's text
        phrase_to_response: the CONVERSATION_PHRASES dict from NLPProcessor
        """
        return phrase_to_response.get(
            matched_phrase,
            "Cooking is always a good topic! What would you like to make?",
        )

    # ------------------------------------------------------------------
    # RESPONSES THAT NEED DATA FROM THE RECIPE DATABASE
    # ------------------------------------------------------------------

    def ingredient_lookup(self, dish_name, ingredients):
        ingredient_lines = "\n".join(f"- {item}" for item in ingredients)
        return (
            f"Bet! Here's what you need for {dish_name}:\n\n"
            f"{ingredient_lines}\n\n"
            f"Ready to cook?"
        )

    def recipe_instructions(self, dish_name, steps):
        step_lines = "\n".join(f"{i}. {step}" for i, step in enumerate(steps, start=1))
        return (
            f"Here's a simple guide for {dish_name}:\n\n"
            f"{step_lines}\n\n"
            f"Enjoy your cooking!"
        )

    def dish_not_found(self):
        return (
            "Hmm, that dish isn't in my recipe book yet! 🍳 "
            "Right now I know: fried rice, spaghetti, chicken adobo, pancakes, and omelette."
        )

    def substitution(self, ingredient_name, alternatives):
        options = ", ".join(alternatives)
        return f"For {ingredient_name}, you could try: {options}."

    def substitution_not_found(self, ingredient_name):
        return (
            f"I don't have a substitute for '{ingredient_name}' in my notes yet, "
            f"sorry! Try checking a trusted recipe site for that one."
        )

    def variant_question(self, dish, variants):
        options = " or ".join(variants)

        return f"What kind of {dish} would you like? {options}?"


    def variant_not_found(self, dish, variants):
        options = " or ".join(variants)

        return (
            f"I didn't recognize that option. "
            f"For {dish}, you can choose: {options}."
        )
