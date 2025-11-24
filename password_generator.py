"""Simple terminal-based password generator."""

import random
import string
from typing import Dict, Tuple


def prompt_yes_no(message: str) -> bool:
    """Prompt the user for a yes/no answer and return True for yes."""
    while True:
        response = input(message).strip().lower()
        if response in {"y", "yes"}:
            return True
        if response in {"n", "no"}:
            return False
        print("Please enter 'y' or 'n'.")


def get_user_preferences() -> Tuple[int, int, Dict[str, str]]:
    """Collect length, quantity, and character type selections from the user."""
    while True:
        length_raw = input("How long should the password be? (minimum 4): ").strip()
        try:
            length = int(length_raw)
            if length < 4:
                print("Password length must be at least 4.")
                continue
        except ValueError:
            print("Please enter a valid number for the length.")
            continue

        count_raw = input("How many passwords to generate? (press Enter for 1): ").strip()
        if count_raw == "":
            count = 1
        else:
            try:
                count = int(count_raw)
                if count < 1:
                    print("Please enter 1 or greater for the number of passwords.")
                    continue
            except ValueError:
                print("Please enter a valid number for how many passwords to generate.")
                continue

        selections = {
            "lowercase": string.ascii_lowercase if prompt_yes_no("Include lowercase letters (y/n): ") else "",
            "uppercase": string.ascii_uppercase if prompt_yes_no("Include uppercase letters (y/n): ") else "",
            "digits": string.digits if prompt_yes_no("Include digits (y/n): ") else "",
            "symbols": string.punctuation if prompt_yes_no("Include symbols (y/n): ") else "",
        }

        chosen_types = [chars for chars in selections.values() if chars]
        if not chosen_types:
            print("You must choose at least one character type.")
            continue

        if length < len(chosen_types):
            print(
                "Password length must be at least the number of selected character types "
                f"({len(chosen_types)})."
            )
            continue

        return length, count, selections


def generate_password(length: int, selections: Dict[str, str]) -> str:
    """Generate a single password meeting the selected criteria."""
    selected_sets = [chars for chars in selections.values() if chars]
    all_characters = "".join(selected_sets)

    # Ensure at least one character from each selected type.
    password_chars = [random.choice(char_set) for char_set in selected_sets]
    remaining_length = length - len(password_chars)
    password_chars.extend(random.choice(all_characters) for _ in range(remaining_length))
    random.shuffle(password_chars)
    return "".join(password_chars)


def main() -> None:
    """Run the interactive password generator."""
    print("Welcome to the Password Generator!")
    while True:
        length, count, selections = get_user_preferences()

        print("\nGenerated passwords:")
        for idx in range(1, count + 1):
            password = generate_password(length, selections)
            print(f"Password {idx}: {password}")

        repeat = prompt_yes_no("\nGenerate more passwords? (y/n): ")
        if not repeat:
            print("Goodbye!")
            break
        print()  # Blank line before next run for readability.


if __name__ == "__main__":
    main()
