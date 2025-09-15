from django.core.exceptions import ValidationError
import datetime
import emoji
import unicodedata
import string

# 3️⃣ Gamify it

# Keep a counter of attempts or time spent (optional).

# Give badges or funny titles depending on how many tries it took.


class UltraStrongPasswordValidator:
    def __init__(self, mothers_maiden_letter='a'):
        self.mothers_maiden_letter = mothers_maiden_letter.lower()
        self.special_chars = "!@#$%^&*()-_+=[]{};:,.<>?/|\\~"
        self.nonexistent_countries = ['Yugoslavia', 'Czechoslovakia', 'Siam', 'Prussia', 'OttomanEmpire', 'EastGermany']
        self.fictional_spaceships = ['MillenniumFalcon', 'Serenity', 'Enterprise', 'Galactica', 'Rocinante']
        self.musical_notes = ['♪', '♫', '♬']
        self.wingdings_characters = ['🂡', '🃏', '✈']
        self.oxford_words = ['apple', 'banana', 'civic', 'turmeric', 'falcon', 'friend']
        self.spices = ['turmeric', 'cumin', 'paprika', 'saffron', 'basil']

    def __call__(self, value: str):
        errors = []

        # Base rules
        if len(value) < 8:
            errors.append("❌ Password is too short. Try at least 8 characters.")

        if not any(c.isupper() for c in value):
            errors.append("❌ Needs at least one uppercase letter.")

        if not any(c in self.special_chars for c in value):
            errors.append("❌ Include at least one special character (!@#...).")

        digits = [int(c) for c in value if c.isdigit()]
        if len(digits) < 3:
            errors.append("❌ Include at least 3 numbers.")

        if not self._is_prime(sum(digits)):
            errors.append(f"❌ Sum of numbers in password ({sum(digits)}) must be a prime number.")

        if any(v in value.lower() for v in 'aeiou'):
            errors.append("❌ Password must not contain any vowels (a, e, i, o, u).")

        if value[0] not in self.special_chars or value[-1] not in self.special_chars:
            errors.append("❌ Start and end your password with a special character.")

        if not any(c in emoji.EMOJI_DATA for c in value):
            errors.append("😂 Must include at least one emoji.")

        if not self._contains_palindrome(value):
            errors.append("🔁 Password must contain a palindrome (at least 3 characters).")

        # letters = [c.lower() for c in value if c.isalpha()]
        # if len(letters) != len(set(letters)):
        #     errors.append("🌀 All alphabet letters must be unique, no repeats.")

        if '90' not in value:
            errors.append("🔢 Include the number '90' (ASCII of Z).")

        if "password" not in value.lower():
            errors.append("😂 Must ironically include the word 'password'.")

        for i in range(1, len(value)):
            if value[i].isalpha() and value[i - 1].isalpha():
                errors.append("🚫 No consecutive letters allowed.")
                break

        # Extended creative rules
        now = datetime.datetime.now()
        if len(value) != now.hour:
            errors.append("⌚ Password length must match the current hour in 24-hour format.")

        if not any(c.lower() in value.lower() for c in self.nonexistent_countries):
            errors.append("🌍 Must contain the name of a country that doesn’t exist anymore.")

        if not any(note in value for note in self.musical_notes):
            errors.append("🎼 Must include at least one musical note character.")

        if now.strftime("%A")[::-1].lower() not in value.lower():
            errors.append("📅 Must contain the current day of the week in reverse.")

        if any(c in 'snake' for c in value.lower()):
            errors.append("🐍 Must NOT contain any letters from the word 'snake'.")

        if not any(ship.lower() in value.lower() for ship in self.fictional_spaceships):
            errors.append("🚀 Must include the name of a fictional spaceship.")

        if not value[0].lower() == self.mothers_maiden_letter:
            errors.append("🧠 First letter must match your mother's maiden name's first letter.")

        if int(len(value)**0.5) ** 2 != len(value):
            errors.append("📏 Password length must be a perfect square.")

        if not any(str(n) in value for n in range(69, 421)):
            errors.append("🎲 Must include a number between 69 and 420.")

        meow_count = sum(1 for c in value.lower() if c in 'meow')
        if not (1 <= meow_count <= 2):
            errors.append("🐱 Must contain at least 1 and at most 2 letters from 'meow'.")

        if not any(ord(c) > 127 for c in value):
            errors.append("🔣 Must have at least one non-English Unicode symbol.")

        ascii_sum = sum(ord(c) for c in value)
        if ascii_sum % 7 != 0:
            errors.append("📉 ASCII sum of all characters must be divisible by 7.")

        if any(c in 'death' for c in value.lower()):
            errors.append("💀 Must NOT include any letters from 'death'.")

        if not self._contains_palindrome(''.join(c for c in value if c.isalnum())):
            errors.append("🧊 Must contain a palindrome of at least 3 characters.")

        if not self._is_calculator_compatible(value):
            errors.append("🪐 Must be readable upside down with calculator digits.")

        if not any(value.startswith(str(score)) for score in [60, 100, 120, 140, 180]):
            errors.append("🎯 Must start with a valid dart score.")

        if not any(spice in value.lower() for spice in self.spices):
            errors.append("🧂 Must include the name of a spice from your kitchen.")

        # Final decision
        if errors:
            raise ValidationError(errors)

    def _is_prime(self, n: int):
        if n < 2: return False
        for i in range(2, int(n ** 0.5) + 1):
            if n % i == 0:
                return False
        return True

    def _contains_palindrome(self, s: str):
        s_clean = ''.join(c.lower() for c in s if c.isalnum())
        n = len(s_clean)
        for i in range(n):
            for j in range(i + 3, n + 1):
                if s_clean[i:j] == s_clean[i:j][::-1]:
                    return True
        return False

    def _is_calculator_compatible(self, s: str):
        calc_map = {'0': '0', '1': '1', '3': 'E', '4': 'h', '5': 'S', '6': '9', '7': 'L', '8': '8', '9': '6'}
        return all(c in calc_map for c in s if c.isdigit())
