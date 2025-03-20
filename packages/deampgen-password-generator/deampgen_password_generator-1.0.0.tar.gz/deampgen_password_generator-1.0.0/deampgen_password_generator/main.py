import random
import string


class PasswordGenerator:
    def __init__(self):
        self.weak_password_length = 4
        self.mid_password_length = 6
        self.strong_password_length = 8
        self.characters = string.digits + string.ascii_letters

    def generate_password(self, length):
        return ''.join(random.choice(self.characters) for _ in range(length))

    def main(self):
        print("What password would you like to generate? (strong/mid/weak)")
        choice = input("Enter a strength of password: (weak/mid/strong): ").strip().lower()

        if choice == 'strong':
            password = self.generate_password(self.strong_password_length)
        elif choice == 'mid':
            password = self.generate_password(self.mid_password_length)
        elif choice == 'weak':
            password = self.generate_password(self.weak_password_length)
        else:
            print("Invalid choice. Please enter 'weak', 'mid', or 'strong'.")
            return

        print(f"Generated password: {password}")