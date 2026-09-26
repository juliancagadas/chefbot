"""
nlp_processor.py

This file defines the NLPProcessor class.

Job of this class (single responsibility):
    - Take raw text the user typed.
    - Clean it up.
    - Break it into tokens (words).
    - Figure out the user's INTENT (what they want).
    - Pull out any useful ENTITY (a dish name, an ingredient name, a
      slang word) from the text.

This is a "rule-based" NLP module: no machine learning, no external
libraries. Everything is done with plain string methods, sets, lists,
and dictionaries. This mirrors, in a simplified way, the classic NLP
pipeline: clean -> tokenize -> classify intent -> extract entities.
"""

import string


class NLPProcessor:
    """Turns raw user text into a cleaned form, tokens, intent, and entities."""

    # ------------------------------------------------------------------
    # SETS of keywords for each intent.
    #
    # We use SETS (not lists) here because we only ever ask
    # "is this word IN the collection?" -- sets answer that question
    # very efficiently, and they also naturally avoid duplicate entries.
    # ------------------------------------------------------------------
    GREETING_WORDS = {"hello", "hi", "hey", "yo", "sup", "yow"}

    GOODBYE_WORDS = {"bye", "goodbye", "exit", "quit"}

    # These are checked as PHRASES (substrings of the cleaned sentence)
    # rather than single tokens, because the meaningful signal is
    # usually more than one word ("what ingredients", "how do i cook").
    SUBSTITUTION_PHRASES = [
        "instead of",
        "substitute",
        "substitution",
        "replace",
        "dont have",
        "don't have",
        "alternative",
        "any other option for",
    ]

    INGREDIENT_LOOKUP_PHRASES = [
        "what ingredients",
        "what's ingredients",
        "which ingredients",
        "ingredients do i need",
        "ingredients for",
        "what do i need",
        "what's in",
        "whats in",
        "ingredient list",
    ]

    RECIPE_INSTRUCTIONS_PHRASES = [
        "how do i cook",
        "how do i make",
        "how to cook",
        "how to make",
        "cooking steps",
        "cooking instructions",
        "procedure for",
        "steps for",
    ]

    CONVERSATION_PHRASES = {
        "cooking is hard": "Real talk! Cooking takes practice, but you got this. "
                            "Start with a simple recipe and build your skills from there.",
        "cooking is difficult": "Real talk! Cooking takes practice, but you got this. "
                                 "Start with a simple recipe and build your skills from there.",
        "favorite food": "I'm all about helping you cook delicious food! "
                          "Fried rice is always a solid choice. 🍳",
        "favourite food": "I'm all about helping you cook delicious food! "
                           "Fried rice is always a solid choice. 🍳",
        "i love cooking": "That's what I like to hear! What are we making today?",
        "i hate cooking": "It grows on you! Pick something easy and quick, "
                           "like an omelette, and go from there.",
        "i am hungry": "Say less! Want me to suggest something quick, like an omelette or fried rice?",
        "i'm hungry": "Say less! Want me to suggest something quick, like an omelette or fried rice?",
    }

    # Slang words are checked as individual tokens, EXCEPT "no cap"
    # which is a two-word phrase and is handled separately so it
    # doesn't get confused with the single word "cap".
    SLANG_WORDS = {"bet", "cap", "slay", "rizz", "sus", "mid"}

    def clean_text(self, text):
        """
        Normalize raw input text.

        Steps:
            1. Convert to lowercase (so "Hello" and "hello" match the same rule).
            2. Strip leading/trailing whitespace.
            3. Collapse multiple internal spaces into one.

        Example:
            "  HOW DO I COOK Fried   Rice?  " -> "how do i cook fried rice?"
        """
        text = text.lower().strip()
        text = " ".join(text.split())  # collapses any run of whitespace to single spaces
        return text

    def tokenize(self, cleaned_text):
        """
        Break cleaned text into a list of word tokens, with punctuation removed.

        Example:
            "how do i cook fried rice?" -> ["how", "do", "i", "cook", "fried", "rice"]
        """
        # Remove punctuation characters like ? ! , . '
        no_punctuation = "".join(
            char for char in cleaned_text if char not in string.punctuation
        )
        tokens = no_punctuation.split()
        return tokens

    def detect_intent(self, cleaned_text, tokens):
        """
        Decide what the user wants, using simple rule-based checks.

        The ORDER of these checks matters: more specific / higher
        priority intents are checked first, so a message that could
        loosely match more than one rule still gets the most useful
        answer.
        """
        token_set = set(tokens)

        # 1) Goodbye - ends the conversation, so check it first.
        if token_set & self.GOODBYE_WORDS:
            return "goodbye"

        # 2) Greeting.
        if token_set & self.GREETING_WORDS or "what's up" in cleaned_text or "whats up" in cleaned_text:
            return "greeting"

        # 3) Ingredient substitution (checked before ingredient_lookup,
        #    since "instead of X" and "what ingredients" are distinct asks).
        if any(phrase in cleaned_text for phrase in self.SUBSTITUTION_PHRASES):
            return "ingredient_substitution"

        # 4) Ingredient lookup.
        if any(phrase in cleaned_text for phrase in self.INGREDIENT_LOOKUP_PHRASES):
            return "ingredient_lookup"

        # 5) Recipe instructions.
        if any(phrase in cleaned_text for phrase in self.RECIPE_INSTRUCTIONS_PHRASES):
            return "recipe_instructions"

        # 6) Slang. "no cap" is checked as a full phrase first so it is
        #    never mistaken for the standalone word "cap".
        if "no cap" in cleaned_text:
            return "slang_response"
        if token_set & self.SLANG_WORDS:
            return "slang_response"

        # 7) General cooking conversation.
        if any(phrase in cleaned_text for phrase in self.CONVERSATION_PHRASES):
            return "cooking_conversation"

        # 8) Nothing matched.
        return "unknown"

    def extract_dish(self, cleaned_text, known_dish_names):
        """
        Look for a known dish name inside the user's text.

        known_dish_names should already be sorted longest-first (see
        RecipeDatabase.get_all_dish_names) so "chicken adobo" is found
        before any shorter, coincidentally-matching word.
        """
        for dish in known_dish_names:
            if dish in cleaned_text:
                return dish
        return None

    # ADD STEP 3 HERE
    def extract_variant(self, cleaned_text, known_variants):
        """Look for a known recipe variant in the user's text."""

        for variant in known_variants:
            if variant in cleaned_text:
                return variant

        return None

    def extract_ingredient(self, cleaned_text, known_ingredient_names):
        """Look for a known ingredient name inside the user's text."""
        for ingredient in known_ingredient_names:
            if ingredient in cleaned_text:
                return ingredient
        return None

    def extract_slang(self, cleaned_text, tokens):
        """Figure out exactly which slang word/phrase was used."""
        if "no cap" in cleaned_text:
            return "no cap"
        for word in tokens:
            if word in self.SLANG_WORDS:
                return word
        return None

    def match_conversation_phrase(self, cleaned_text):
        """Return the predefined conversation phrase found in the text, if any."""
        for phrase in self.CONVERSATION_PHRASES:
            if phrase in cleaned_text:
                return phrase
        return None
