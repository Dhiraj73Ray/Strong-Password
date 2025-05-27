from django import forms
import emoji
import string

class StrongPassword(forms.Form):
    password = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'pass-input',
            'placeholder': 'Enter Strong Password...',
            'autocomplete': 'off',
        })
    )

    def clean_password(self):
        import datetime
        value = self.cleaned_data.get('password')
        now = datetime.datetime.now()

        if len(value) < 8:
            raise forms.ValidationError("❌ Password is too short. Try at least 8 characters.")

        if not any(c.isupper() for c in value):
            raise forms.ValidationError("❌ Needs at least one uppercase letter.")

        if not any(c in "!@#$%^&*()-_+=[]{};:,.<>?/|\\~" for c in value):
            raise forms.ValidationError("❌ Include at least one special character (!@#...).")

        digits = [int(c) for c in value if c.isdigit()]
        if len(digits) < 3:
            raise forms.ValidationError("❌ Include at least 3 numbers.")

        def is_prime(n):
            if n < 2: return False
            for i in range(2, int(n ** 0.5) + 1):
                if n % i == 0:
                    return False
            return True
        if not is_prime(sum(digits)):
            raise forms.ValidationError(f"❌ Sum of numbers in password ({sum(digits)}) must be a prime number.")

        if any(v in value.lower() for v in 'aeiou'):
            raise forms.ValidationError("❌ Password must not contain any vowels (a, e, i, o, u).")

        if value[0] not in "!@#$%^&*" or value[-1] not in "!@#$%^&*":
            raise forms.ValidationError("❌ Start and end your password with a special character.")

        if not any(c in emoji.EMOJI_DATA for c in value):
            raise forms.ValidationError("😂 Must include at least one emoji.")

        # # Rule 10: Palindrome
        # stripped = ''.join(c.lower() for c in value if c.isalnum())
        # if stripped != stripped[::-1]:
        #     raise forms.ValidationError("🔁 Password must be a palindrome.")
        stripped = ''.join(c.lower() for c in value if c.isalnum())
        def contains_palindrome(s):
            n = len(s)
            for i in range(n):
                for j in range(i + 3, n + 1):  # palindromes of length 3 or more
                    substr = s[i:j]
                    if substr == substr[::-1]:
                        return True
            return False
        if not contains_palindrome(stripped):
            raise forms.ValidationError("🔁 Password must contain a palindrome (at least 3 characters).")

        letters = [c.lower() for c in value if c.isalpha()]
        if len(letters) != len(set(letters)):
            raise forms.ValidationError("🌀 All alphabet letters must be unique, no repeats.")

        if '90' not in value:
            raise forms.ValidationError("🔢 Include the number '90' (ASCII of Z).")

        if "password" not in value.lower():
            raise forms.ValidationError("😂 Must ironically include the word 'password'.")

        for i in range(1, len(value)):
            if value[i].isalpha() and value[i - 1].isalpha():
                raise forms.ValidationError("🚫 No consecutive letters allowed.")
        
        if sum(1 for c in value if c.isupper()) != 2:
            raise forms.ValidationError("🔠 Password must contain exactly 2 uppercase letters.")

        if not any(c.isdigit() and int(c) % 3 == 0 for c in value):
            raise forms.ValidationError("➗ Include at least one digit divisible by 3 (e.g., 3, 6, 9).")

        if "admin" in value.lower():
            raise forms.ValidationError("👮 Password must not contain the word 'admin'.")

        if value.count("-") != 1:
            raise forms.ValidationError("➖ Include exactly one dash (-).")

        if len(value) % 4 != 0:
            raise forms.ValidationError("🔢 Password length must be a multiple of 4.")

        from collections import Counter
        counts = Counter(value)
        if not any(v == 3 for v in counts.values()):
            raise forms.ValidationError("🔁 Include one character exactly 3 times.")

        if ' ' in value:
            raise forms.ValidationError("⛔ No spaces allowed in the password.")

        if not value[-1].isdigit():
            raise forms.ValidationError("🔚 Password must end with a number.")

        mid = len(value) // 2
        if not value[mid].isalpha():
            raise forms.ValidationError("💡 The middle character must be a letter.")

        if not any(c in "abcdefABCDEF" for c in value):
            raise forms.ValidationError("🔣 Include at least one hex letter (a-f).")

        if not any(value[i] == value[i + 1] for i in range(len(value) - 1)):
            raise forms.ValidationError("🪞 Include at least one mirrored character pair (like 'aa', 'bb').")

        if sum(ord(c) for c in value) % 2 != 0:
            raise forms.ValidationError("⚖️ ASCII sum of password characters must be even.")

        digits = [c for c in value if c.isdigit()]
        if len(digits) != len(set(digits)):
            raise forms.ValidationError("🔂 No digit should repeat.")

        if not any(c in "nopqrstuvwxyz" for c in value.lower()):
            raise forms.ValidationError("🔡 Include at least one letter from n-z.")

        if not any(c in ".,;:" for c in value):
            raise forms.ValidationError("✍️ Include at least one punctuation mark (.,;:).")

        types = [c.isalpha() for c in value[:3]], [c.isdigit() for c in value[:3]], [not c.isalnum() for c in value[:3]]
        if sum(any(t) for t in types) < 3:
            raise forms.ValidationError("🎭 First three characters must be letter, digit, and symbol.")

        if not any(c in '01' for c in value):
            raise forms.ValidationError("💻 Include at least one binary digit (0 or 1).")

        specials = [c for c in value if not c.isalnum()]
        if len(specials) % 2 == 0:
            raise forms.ValidationError("🧮 Total special characters must be an odd number.")

        reversed_words = ['dog', 'stressed', 'evil']
        if not any(w[::-1] in value.lower() for w in reversed_words):
            raise forms.ValidationError("🔄 Include a reversed real word like 'god', 'stressed', or 'live'.")

        if not any(c in "αβγδεζηθλμνξοπρστυφχψω" for c in value):
            raise forms.ValidationError("🧿 Include at least one Greek letter (α-ω).")
        
        if len(value) != now.hour:
            raise forms.ValidationError(f"⌚ Password length must be exactly {now.hour} characters (current hour).")

        old_countries = ["yugoslavia", "czechoslovakia", "east germany", "ussr", "ottoman empire"]
        if not any(country in value.lower() for country in old_countries):
            raise forms.ValidationError("🌍 Must contain a country name that no longer exists (e.g., Yugoslavia).")

        musical_notes = "♪♫♬"
        if not any(c in musical_notes for c in value):
            raise forms.ValidationError("🎼 Include at least one musical note character (♪ ♫ ♬).")

        day_reversed = now.strftime("%A")[::-1].lower()
        if day_reversed not in value.lower():
            raise forms.ValidationError(f"📅 Must contain the current weekday reversed: '{day_reversed}'.")

        forbidden_letters = set("snake")
        if any(c.lower() in forbidden_letters for c in value):
            raise forms.ValidationError("🐍 Password must NOT contain letters from the word 'snake'.")

        ships = ["millenniumfalcon", "enterprise", "serenity", "galactica", "defiant"]
        if not any(ship in value.lower() for ship in ships):
            raise forms.ValidationError("🚀 Must include a fictional spaceship name (e.g., MillenniumFalcon).")

        mother_maiden_first = self.cleaned_data.get('mother_maiden_first_letter')
        if mother_maiden_first and value[0].lower() != mother_maiden_first.lower():
            raise forms.ValidationError(f"🧠 Password must start with '{mother_maiden_first.upper()}', your mother's maiden name first letter.")

        length = len(value)
        if int(length**0.5)**2 != length:
            raise forms.ValidationError("📏 Password length must be a perfect square (4, 9, 16, 25...).")

        import re
        numbers = [int(num) for num in re.findall(r'\d+', value)]
        if not any(69 <= num <= 420 for num in numbers):
            raise forms.ValidationError("🎲 Must include a number between 69 and 420 (inclusive).")

        meow_letters = set("meow")
        count_meow = sum(1 for c in value.lower() if c in meow_letters)
        if count_meow == 0 or count_meow > 2:
            raise forms.ValidationError("🐱 Must contain at least 1 but no more than 2 letters from 'meow'.")

        if all(ord(c) < 128 for c in value):
            raise forms.ValidationError("🔣 Must have at least one non-English Unicode character (e.g., Ж, 你, ø).")

        if sum(ord(c) for c in value) % 7 != 0:
            raise forms.ValidationError("📉 ASCII sum of all characters must be divisible by 7.")

        if any(c in "death" for c in value.lower()):
            raise forms.ValidationError("💀 Password must NOT contain letters from the word 'death'.")

        def contains_palindrome_word(s):
            words = re.findall(r'[a-zA-Z]{3,}', s.lower())
            for w in words:
                if w == w[::-1]:
                    return True
            return False
        if not contains_palindrome_word(value):
            raise forms.ValidationError("🧊 Must contain a palindrome word (e.g., 'civic', 'madam').")

        upside_down_map = {'0':'0', '1':'1', '6':'9', '8':'8', '9':'6'}
        filtered = [c for c in value if c in upside_down_map]
        flipped = ''.join(upside_down_map[c] for c in reversed(filtered))
        if ''.join(filtered) != flipped:
            raise forms.ValidationError("🪐 Password must read the same upside down using calculator letters (0,1,6,8,9).")

        valid_dart_scores = ["180", "60", "100", "120", "140", "150", "170"]
        if not any(value.startswith(score) for score in valid_dart_scores):
            raise forms.ValidationError("🎯 Password must start with a valid dart score (e.g., 180).")

        spices = ["turmeric", "cumin", "cinnamon", "pepper", "clove", "nutmeg", "ginger"]
        if not any(spice in value.lower() for spice in spices):
            raise forms.ValidationError("🧂 Must include the name of a spice from your kitchen (e.g., turmeric).")

        wingdings_chars = "🂡🃏✈"
        if not any(c in wingdings_chars for c in value):
            raise forms.ValidationError("🤡 Must contain at least one Wingdings font character (🂡🃏✈).")

        
        dictionary = ["apple", "banana", "orange", "grape", "melon"]
        reversed_words = [w[::-1] for w in dictionary]
        if not any(rw in value.lower() for rw in reversed_words):
            raise forms.ValidationError("📚 Must include at least one reversed valid word from the Oxford Dictionary (apple, banana...).")


        return value

