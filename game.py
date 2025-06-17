import random


categories = {
    "fruits": [
        "apple", "banana", "cherry", "dates", "melon", "watermelon", "grape", "orange",
        "papaya", "pineapple", "kiwi", "pear", "peach", "plum", "guava", "mango",
        "fig", "apricot", "blueberry", "blackberry", "strawberry", "raspberry", "lychee"
    ],
    "cars": [
        "audi", "tesla", "bmw", "mustang", "ferrari", "lamborghini", "porsche", "nissan",
        "toyota", "honda", "volkswagen", "mercedes", "chevrolet", "hyundai", "jaguar"
    ],
    "animals": [
        "tiger", "elephant", "giraffe", "kangaroo", "zebra", "lion", "leopard", "panda",
        "rhinoceros", "hippopotamus", "monkey", "cheetah", "deer", "bear", "fox"
    ]
}

vowels = "aeiou"
total_points = 0

print("Available categories:")
for cat in categories:
    print(f"- {cat}")

selected = input("\nChoose a category: ").strip().lower()

if selected not in categories:
    print("Invalid category selected.")
else:
    words = categories[selected]
    word = random.choice(words)
    wordlen = len(word)
    points = 0

    print("-" * wordlen)
    guess = input("Guess the word: ").strip().lower()

    if guess == word:
        points = 5
        print("Correct on first try!")
    else:
       
        hint = word[0] + "-" * (wordlen - 1)
        print(f"Hint: {hint}")
        guess = input("Second try: ").strip().lower()

        if guess == word:
            points = 2
            print("Correct on second try!")
        else:
            hint = ""
            for idx, char in enumerate(word):
                if char in vowels or idx == wordlen - 1:
                    hint += char
                else:
                    hint += "-"
            print(f"Final hint: {hint}")
            guess = input("Last try: ").strip().lower()

            if guess == word:
                points = 1
                print("Correct on last try!")
            else:
                print("Incorrect. No more tries.")

    print(f"The word was: {word}")
    print(f"Points earned: {points}")
    total_points += points
    print(f"Total Score: {total_points} points")
