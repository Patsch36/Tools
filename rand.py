import argparse
import random
import string
import pyperclip

class RandomStringGenerator:
    def __init__(self, length: int, use_digits: bool, use_uppercase: bool, use_lowercase: bool, use_signs: bool):
        self.length = length
        self.use_digits = use_digits
        self.use_uppercase = use_uppercase
        self.use_lowercase = use_lowercase
        self.use_signs = use_signs

    def generate(self) -> str:
        """Generates a random string based on specified criteria."""
        char_set = self._get_character_set()
        if not char_set:
            raise ValueError("At least one character type must be selected.")
        return ''.join(random.choice(char_set) for _ in range(self.length))

    def _get_character_set(self) -> str:
        """Builds character set based on the selected options."""
        char_set = ""
        if self.use_uppercase:
            char_set += string.ascii_uppercase
        if self.use_lowercase:
            char_set += string.ascii_lowercase
        if self.use_digits:
            char_set += string.digits
        if self.use_signs:
            char_set += string.punctuation
        return char_set


def parse_arguments() -> argparse.Namespace:
    """Parses command line arguments for the script."""
    parser = argparse.ArgumentParser(description="Generate random strings")
    parser.add_argument(
        '-l', '--length', 
        type=int, 
        default=8, 
        help="Length of the random string (default: 8)"
    )
    parser.add_argument(
        '--digits', 
        action='store_false', 
        default=True, 
        help="Include digits in the string (default: True)"
    )
    parser.add_argument(
        '--uppercase', 
        action='store_false', 
        default=True, 
        help="Include uppercase letters in the string (default: True)"
    )
    parser.add_argument(
        '--lowercase', 
        action='store_false', 
        default=True, 
        help="Include lowercase letters in the string (default: True)"
    )
    parser.add_argument(
        '--signs',
        action='store_false',
        default=True,
        help="Include signs (punctuation) in the string (default: False)"
    )
    
    args = parser.parse_args()
    return args


def main():
    """Main entry point of the script."""
    args = parse_arguments()
    
    # If no character types are selected, raise an error
    if not (args.digits or args.uppercase or args.lowercase or args.signs):
        print("Error: At least one character type must be included (digits, uppercase, lowercase, signs).")
        return

    generator = RandomStringGenerator(
        length=args.length,
        use_digits=args.digits,
        use_uppercase=args.uppercase,
        use_lowercase=args.lowercase,
        use_signs=args.signs
    )
    
    random_string = generator.generate()
    print(f"Generated random string: {random_string}")
    pyperclip.copy(random_string)


if __name__ == "__main__":
    main()