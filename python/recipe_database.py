"""
recipe_database.py

This file defines the RecipeDatabase class.

Job of this class (single responsibility):
    - Hold all the "facts" ChefBot knows: recipes and ingredient substitutions.
    - Answer simple questions like "do you know this dish?" or
      "what can replace butter?"

Why a separate class?
    Keeping DATA (the recipes) separate from LOGIC (how we understand
    the user, how we reply) makes the program much easier to read and
    extend. If you want to add a new dish later, you only ever touch
    this one file.
"""


class RecipeDatabase:
    """Stores recipe information and ingredient substitutions."""

    def __init__(self):
        # --------------------------------------------------------------
        # DICTIONARY of recipes.
        # Structure:  dish name (str) -> { "ingredients": [...], "steps": [...] }
        #
        # We use a dictionary here because we always look things up by
        # NAME ("fried rice", "pancakes", ...). Dictionaries give us
        # fast "key -> value" lookup, which is exactly what we need.
        #
        # Inside each dish, "ingredients" and "steps" are LISTS because
        # order matters for steps, and a simple ordered collection is
        # the natural fit for "a bunch of ingredients" too.
        # --------------------------------------------------------------
        self._recipes = {
            "fried rice": {
                "ingredients": [
                    "cooked rice (preferably a day old)",
                    "eggs",
                    "garlic, minced",
                    "onion, chopped",
                    "soy sauce",
                    "cooking oil",
                ],
                "steps": [
                    "Heat oil in a pan over medium heat.",
                    "Sauté the garlic and onion until fragrant.",
                    "Push them to the side, then scramble the eggs in the same pan.",
                    "Add the rice and break up any clumps.",
                    "Pour in soy sauce and mix everything together.",
                    "Stir-fry for a few more minutes, then serve hot.",
                ],
            },
            "spaghetti": {
                "ingredients": [
                    "spaghetti noodles",
                    "ground meat (beef or pork)",
                    "tomato sauce",
                    "onion, chopped",
                    "garlic, minced",
                    "cheese for topping",
                ],
                "steps": [
                    "Boil the spaghetti noodles according to the package instructions.",
                    "In a separate pan, sauté garlic and onion.",
                    "Add the ground meat and cook until browned.",
                    "Pour in the tomato sauce and simmer for about 15 minutes.",
                    "Combine the sauce with the cooked noodles.",
                    "Top with cheese before serving.",
                ],
            },


            "adobo": {
                "variants": {
                    "chicken": {
                        "ingredients": [
                            "chicken pieces",
                            "soy sauce",
                            "vinegar",
                            "garlic, crushed",
                            "bay leaves",
                            "whole peppercorns",
                        ],
                        "steps": [
                            "Combine chicken, soy sauce, vinegar, garlic, bay leaves, and peppercorns in a pot.",
                            "Let it marinate for at least 15-30 minutes if you have time.",
                            "Bring the pot to a boil, then lower the heat to a simmer.",
                            "Simmer until the chicken is cooked through and tender.",
                            "Continue simmering uncovered to let the sauce reduce and thicken.",
                            "Serve warm with rice.",
                        ],
                    },

                    "pork": {
                        "ingredients": [
                            "pork belly",
                            "soy sauce",
                            "vinegar",
                            "garlic, crushed",
                            "bay leaves",
                            "whole peppercorns",
                        ],
                        "steps": [
                            "Combine pork, soy sauce, vinegar, garlic, bay leaves, and peppercorns in a pot.",
                            "Let it marinate for at least 15-30 minutes if you have time.",
                            "Bring the pot to a boil, then lower the heat to a simmer.",
                            "Cook until the pork becomes tender.",
                            "Continue simmering uncovered until the sauce reduces and thickens.",
                            "Serve warm with rice.",
                        ],
                    },
                }
            },

            "pancakes": {
                "ingredients": [
                    "flour",
                    "milk",
                    "egg",
                    "sugar",
                    "baking powder",
                ],
                "steps": [
                    "Mix the flour, sugar, and baking powder in a bowl.",
                    "In another bowl, whisk together the milk and egg.",
                    "Combine the wet and dry ingredients until just mixed (a few lumps are fine).",
                    "Heat a lightly oiled pan over medium heat.",
                    "Pour batter onto the pan and cook until bubbles form, then flip.",
                    "Cook the other side until golden, then serve.",
                ],
            },
            "omelette": {
                "ingredients": [
                    "eggs",
                    "salt",
                    "pepper",
                    "cooking oil or butter",
                    "optional fillings (cheese, ham, vegetables)",
                ],
                "steps": [
                    "Crack the eggs into a bowl and beat with a bit of salt and pepper.",
                    "Heat oil or butter in a non-stick pan over medium-low heat.",
                    "Pour in the eggs and let them set slightly at the edges.",
                    "Add your fillings onto one half of the eggs.",
                    "Fold the omelette in half once mostly set.",
                    "Slide onto a plate and serve immediately.",
                ],
            },
        }


        # DICTIONARY of substitutions.
        # Structure: ingredient name (str) -> list of possible REPLACEMENTT
        self._substitutions = {
            "butter": ["margarine", "vegetable oil", "coconut oil"],
            "milk": ["evaporated milk diluted with water", "soy milk", "powdered milk mixed with water"],
            "sugar": ["honey", "brown sugar", "condensed milk (use less liquid elsewhere)"],
            "egg": ["mashed banana (for baking)", "1/4 cup applesauce", "a mix of flour and water as a binder"],
            "soy sauce": ["fish sauce (use less, it's saltier)", "worcestershire sauce", "salt with a splash of water"],
            "vinegar": ["lemon juice", "lime juice", "calamansi juice"],
            "garlic": ["garlic powder", "shallots", "onion (in a pinch)"],
        }

    # --------------------------------------------------------------
    # RECIPE-RELATED METHODS
    # --------------------------------------------------------------

    def has_recipe(self, dish_name):
        """Return True if we know this dish."""
        return dish_name in self._recipes

    def get_ingredients(self, dish_name):
        """Return the ingredient list for a dish, or None if unknown."""
        recipe = self._recipes.get(dish_name)
        return recipe["ingredients"] if recipe else None

    def get_steps(self, dish_name):
        """Return the cooking steps for a dish, or None if unknown."""
        recipe = self._recipes.get(dish_name)
        return recipe["steps"] if recipe else None


    #add 1
    def has_variants(self, dish_name):
        """Return True if a dish has multiple variants."""
        recipe = self._recipes.get(dish_name)

        return recipe is not None and "variants" in recipe

    def get_variants(self, dish_name):
        """Return the available variants for a dish."""
        recipe = self._recipes.get(dish_name)

        if recipe and "variants" in recipe:
            return list(recipe["variants"].keys())
        
        return None

    def get_variant_recipe(self, dish_name, variant):
        """Return a specific recipe variant."""
        recipe = self._recipes.get(dish_name)

        if recipe and "variants" in recipe:
            return recipe["variants"].get(variant)

        return None
    

    def get_all_dish_names(self):
        """
        Return every dish name we know about.

        We sort by length (longest first) so that when we later search
        user text for a dish name, "chicken adobo" is checked before a
        shorter word that might accidentally be a substring of it.
        """
        return sorted(self._recipes.keys(), key=len, reverse=True)

    # --------------------------------------------------------------
    # SUBSTITUTION-RELATED METHODS
    # --------------------------------------------------------------

    def has_substitution(self, ingredient_name):
        """Return True if we know a substitute for this ingredient."""
        return ingredient_name in self._substitutions

    def get_substitution(self, ingredient_name):
        """Return the list of substitute suggestions, or None if unknown."""
        return self._substitutions.get(ingredient_name)

    def get_all_ingredient_names(self):
        """Return every ingredient name we have substitutions for."""
        return sorted(self._substitutions.keys(), key=len, reverse=True)
