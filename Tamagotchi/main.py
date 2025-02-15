# Pet Program

from random import randrange
import tkinter as tk
from tkinter import ttk  # For themed widgets
from tkinter import PhotoImage


class Pet(object):
    def __init__(self, name, animal_type):
        self.name = name
        self.animal_type = animal_type
        self.food = 50
        self.food_max = 100
        self.food_warning = 20
        self.excitement = 50
        self.excitement_max = 100
        self.excitement_warning = 20
        self.vocab = ["Hello!", "I'm happy!", "Let's play!"]
        self.alive = True

    def feed(self):
        if not self.alive:
            return
        self.food += 10
        if self.food > self.food_max:
            self.food = self.food_max

    def talk(self):
        if not self.alive:
            return
        self.excitement -= 5
        if self.excitement < 0:
            self.excitement = 0

    def play(self):
        if not self.alive:
            return
        self.excitement += 10
        self.food -= 5
        if self.food < 0:
            self.food = 0
        if self.excitement > self.excitement_max:
            self.excitement = self.excitement_max
        if self.food == 0:
            self.alive = False

    def teach(self, new_word):
        if not self.alive:
            return
        self.vocab.append(new_word)

    def mood(self):
        if not self.alive:
            return "Deceased"
        if self.food < self.food_warning or self.excitement < self.excitement_warning:
            return "Unhappy"
        return "Happy"


def get_pet_info():
    # Create hidden root window
    root = tk.Tk()
    root.withdraw()
    
    # Create input window
    input_window = tk.Toplevel(root)
    input_window.title("Create Your Pet")

    # Load and display tamagotchi egg image
    egg_image = PhotoImage(file="tamagochi egg.png")
    egg_label = tk.Label(input_window, image=egg_image)
    egg_label.image = egg_image  # Keep a reference to avoid garbage collection
    egg_label.grid(row=0, column=0, columnspan=2, pady=10)




    
    # Name input
    tk.Label(input_window, text="Pet Name:").grid(row=1, column=0, padx=5, pady=5)

    name_entry = tk.Entry(input_window)
    name_entry.grid(row=1, column=1, padx=5, pady=5)
    
    # Type input
    tk.Label(input_window, text="Pet Type:").grid(row=2, column=0, padx=5, pady=5)

    type_entry = tk.Entry(input_window)
    type_entry.grid(row=2, column=1, padx=5, pady=5)

    
    # Submit button
    def submit():
        nonlocal pet_name, pet_type
        pet_name = name_entry.get().strip()
        pet_type = type_entry.get().strip()
        if pet_name and pet_type:
            input_window.destroy()
    
    pet_name = ""
    pet_type = ""
    tk.Button(input_window, text="Create Pet", command=submit).grid(row=3, column=0, columnspan=2, pady=10)

    
    # Wait for window to close
    input_window.wait_window()
    return pet_name, pet_type

def main():
    pet_name, pet_type = get_pet_info()
    if not pet_name or not pet_type:
        return
    
    my_pet = Pet(pet_name, pet_type)

    # --- GUI Setup ---
    window = tk.Tk()


    window.title("Virtual Pet")

    # Style configuration for a more modern look (optional)
    style = ttk.Style()
    style.theme_use('clam')  # Or 'alt', 'default', 'classic'

    # Labels to display pet info
    name_label = ttk.Label(window, text=f"Name: {my_pet.name}")
    name_label.pack(pady=5)

    type_label = ttk.Label(window, text=f"Type: {my_pet.animal_type}")
    type_label.pack(pady=5)

    mood_label = ttk.Label(window, text=f"Mood: {my_pet.mood()}")  # Initial mood
    mood_label.pack(pady=5)

    food_label = ttk.Label(window, text=f"Food: {my_pet.food}")
    food_label.pack(pady=5)

    excitement_label = ttk.Label(window, text=f"Excitement: {my_pet.excitement}")
    excitement_label.pack(pady=5)

    # Text area to display pet's speech
    speech_text = tk.Text(window, height=5, width=30, wrap=tk.WORD)  # wrap prevents text from going off screen
    speech_text.pack(pady=10)

    # Functions to update labels
    def update_labels():
        mood_label.config(text=f"Mood: {my_pet.mood()}")
        food_label.config(text=f"Food: {my_pet.food}")
        excitement_label.config(text=f"Excitement: {my_pet.excitement}")
        if not my_pet.alive:
            for button in [feed_button, talk_button, teach_button, play_button]:
                button.config(state=tk.DISABLED)

    def display_speech(text):
        speech_text.insert(tk.END, text + "\n")  # Add new speech to the end
        speech_text.see(tk.END)  # Scroll to the bottom to show the newest speech

    # Button functions
    def feed_pet():
        my_pet.feed()
        update_labels()
        display_speech("*Nomnomnomnom* \n Mmmmmmm. Thank you!")
        if my_pet.food == my_pet.food_max:
            display_speech("I'm full!")
        elif my_pet.food < my_pet.food_warning:
            display_speech("I'm still hungry!")

    def talk_to_pet():
        my_pet.talk()
        update_labels()
        display_speech(my_pet.vocab[randrange(len(my_pet.vocab))])

    def teach_word():
        new_word = teach_entry.get()
        if new_word: # Check if the entry is not empty
            my_pet.teach(new_word)
            update_labels()
            display_speech(f"You taught {my_pet.name} the word: {new_word}")
            teach_entry.delete(0, tk.END)  # Clear the entry field
        else:
            display_speech("Please enter a word to teach.")

    def play_with_pet():
        my_pet.play()
        update_labels()
        if not my_pet.alive:
            display_speech("Your pet has passed away")
        else:
            display_speech("Woohoo!")
            if my_pet.excitement == my_pet.excitement_max:
                display_speech("I'm really happy!")
            elif my_pet.excitement < my_pet.excitement_warning:
                display_speech("I'm bored")

    # Buttons
    feed_button = ttk.Button(window, text="Feed", command=feed_pet)
    feed_button.pack(pady=5)

    talk_button = ttk.Button(window, text="Talk", command=talk_to_pet)
    talk_button.pack(pady=5)

    teach_frame = tk.Frame(window)  # Frame for the entry and button
    teach_frame.pack()
    teach_entry = ttk.Entry(teach_frame)
    teach_entry.pack(side=tk.LEFT)
    teach_button = ttk.Button(teach_frame, text="Teach", command=teach_word)
    teach_button.pack(side=tk.LEFT)

    play_button = ttk.Button(window, text="Play", command=play_with_pet)
    play_button.pack(pady=5)

    # Quit button with delayed close
    def quit_program():
        display_speech("Goodbye")
        window.after(3000, window.destroy)
        
    quit_button = ttk.Button(window, text="Quit", command=quit_program)
    quit_button.pack(pady=5)

    update_labels() # Update the labels at the beginning


    window.mainloop()  # Start the GUI event loop


main()
