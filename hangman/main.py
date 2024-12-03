import tkinter as tk
from tkinter import simpledialog
from PIL import Image, ImageTk
import random

class HangmanGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Hangman Game")
        
        self.category = self.choose_category()
        self.word = self.importwords(self.category)
        self.guesses = []
        self.max_attempts = 10
        self.attempts = 0
        
        self.image_label = tk.Label(root)
        self.image_label.pack(pady=10)
        
        self.update_image()
        
        self.word_label = tk.Label(root, text="_ " * len(self.word), font=("Helvetica", 24))
        self.word_label.pack(pady=10)
        
        self.entry = tk.Entry(root)
        self.entry.pack(pady=10)
        
        self.guess_button = tk.Button(root, text="Guess", command=self.make_guess)
        self.guess_button.pack(pady=10)
        
        self.reset_button = tk.Button(root, text="Reset", command=self.reset_game)
        self.reset_button.pack(pady=10)
        
        self.message_label = tk.Label(root, text="")
        self.message_label.pack(pady=10)
        
    
    def choose_category(self):
        categories = ["brands", "famouspeople", "objects"]
        category = simpledialog.askstring("Choose Category", "Choose a category: brands, famouspeople, objects")
        while category not in categories:
            category = simpledialog.askstring("Choose Category", "Invalid category. Choose a category: brands, famouspeople, objects")
        return category
    
    def update_image(self):
        image_path = f"imgs/{self.attempts}.jpg"
        image = Image.open(image_path)
        photo = ImageTk.PhotoImage(image)
        self.image_label.config(image=photo)
        self.image_label.image = photo
    
    def make_guess(self):
        guess = self.entry.get().upper()
        self.entry.delete(0, tk.END)
        
        if len(guess) != 1 or not guess.isalpha():
            self.message_label.config(text="Please enter a single letter.")
            return
        
        if guess in self.guesses:
            self.message_label.config(text="You already guessed that letter.")
            return
        
        self.guesses.append(guess)
        
        if guess in self.word:
            self.update_word_label()
            if "_" not in self.word_label.cget("text"):
                self.message_label.config(text="You win!")
        else:
            self.attempts += 1
            self.update_image()
            if self.attempts >= self.max_attempts:
                self.message_label.config(text="You lose! The word was " + self.word)
    
    def update_word_label(self):
        display_word = ""
        for letter in self.word:
            if letter in self.guesses:
                display_word += letter + " "
            else:
                display_word += "_ "
        self.word_label.config(text=display_word)
    
    def importwords(self, category):
        try:
            with open(f'lists/{category}.txt', 'r') as f:
                words = f.read().splitlines()
                return random.choice(words).upper()
        except FileNotFoundError:
            return "UNKNOWN"
    
    def reset_game(self):
        self.category = self.choose_category()
        self.word = self.importwords(self.category)
        self.guesses = []
        self.attempts = 0
        self.update_image()
        self.word_label.config(text="_ " * len(self.word))
        self.message_label.config(text="")

if __name__ == "__main__":
    root = tk.Tk()
    game = HangmanGame(root)
    root.mainloop()