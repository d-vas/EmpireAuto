import tkinter as tk

# Create the main application window
root = tk()
root.title("My Tkinter App")  # Set the title

# Create widgets (buttons, labels, etc.) and add them to the window
label = tk.Label(root, text="Hello, Tkinter!")
button = tk.Button(root, text="Click Me")

# Pack the widgets to place them in the window
label.pack()
button.pack()

# Define event handlers (functions that are called when events occur)
def button_click():
    label.config(text="Button clicked!")

# Bind the event handler to the button
button.config(command=button_click)

# Start the main event loop
root.mainloop()
