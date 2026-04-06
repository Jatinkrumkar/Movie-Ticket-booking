import tkinter as tk
from tkinter import messagebox, ttk
import json
import random

# --- Basic Data ---
movielist = {"Avengers: Endgame": (100, ["10:00", "14:00", "17:30"]), "Avengers": (200, ["11:00", "13:40"])}
movies = list(movielist.keys())
prices = list(i[0] for i in movielist.values())

MOVIE_NAME = movies[0]
TICKET_PRICE = prices[0]
TIME = movielist[movies[0]][1][0]
# 0 = Available, 1 = Booked. Let's use 10 seats.
# (I've pre-booked seats 3 and 7 for demonstration)
seat_status = { "Avengers: Endgame":
                    {"10:00":
                        [
                            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
                        ],
                     "14:00":
                        [
                            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
                        ],
                     "17:30":
                        [
                            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
                        ]
                    }, 
                "Avengers":
                    {"11:00":
                        [
                            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
                        ],
                     "13:40":
                        [
                            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
                        ]
                    }
                }
selected_seats = []
buttons = []
try:
    with open("seats.json", 'r') as f:
        seat_status = json.load(f)
except:
    with open("seats.json", 'w') as f:
        json.dump(seat_status, f)

def toggle_seat(idx, btn):
    """Handles clicking a seat button."""
    if seat_status[MOVIE_NAME][TIME][idx] == 1:
        messagebox.showinfo("Unavailable", "This seat is already booked!")
        return

    if idx in selected_seats:
        selected_seats.remove(idx) # Deselect
        btn.config(bg="green") 
    else:
        selected_seats.append(idx) # Select
        btn.config(bg="blue") 

def book_tickets():
    """Calculates price and confirms booking."""
    if not selected_seats:
        messagebox.showwarning("No Seats", "Please select at least one seat.")
        return

    base_price = len(selected_seats) * TICKET_PRICE
    fee = base_price * 0.10 # 10% Convenience Fee
    total = base_price + fee

    # Create receipt text
    seat_numbers = [s + 1 for s in selected_seats] # Add 1 so seats start at 1, not 0
    receipt = f"Movie: {MOVIE_NAME}\n"
    receipt += f"Seats: {seat_numbers}\n"
    receipt += f"Total: ₹{total:.2f}\n\nConfirm Booking?"

    # Show confirmation popup
    if messagebox.askyesno("Confirm", receipt):
        # Update seat status to booked (1) and turn buttons red
        show_payment_gateway(total)

def showseats(moviename, seat_frame):
    for widget in seat_frame.winfo_children():
        widget.destroy()
    global buttons
    buttons = []

    
    for i in range(40):
        row = i // 10
        col = i % 10
        s = 15 if col == 3 or col == 7 else 0
        btn = tk.Button(seat_frame, text=str(i+1), width=4, height=2)
        
        if seat_status[moviename][TIME][i] == 1:
            btn.config(bg="red")
        else:
            btn.config(bg="green")
            
        # Command to run when button is clicked
        btn.config(command=lambda idx=i, b=btn: toggle_seat(idx, b))
        btn.grid(row=row, column=col, padx=(5+s, 5), pady=5)
        buttons.append(btn)

def selection_changed(event):
    sel = cb.get()
    lbl.config(text=sel)
    global TICKET_PRICE, MOVIE_NAME, TIME
    TICKET_PRICE = movielist[sel][0]
    MOVIE_NAME = sel
    TIME = movielist[sel][1][0]
    cb1["values"] = movielist[sel][1]
    cb1.current(0)
    showseats(sel, seat_frame)
    pricelbl.config(text=f"Price: ₹{movielist[sel][0]}")

def time_changed(event):
    sel = cb1.get()
    global TIME
    TIME = sel
    showseats(MOVIE_NAME, seat_frame)


def show_payment_gateway(total_amount):
    """Opens a new window to simulate UPI/QR Payment."""
    # Create a new pop-up window
    pay_window = tk.Toplevel(root)
    pay_window.title("Payment Gateway")
    pay_window.geometry("300x400")
    pay_window.grab_set() # Forces the user to interact with this window only
    
    tk.Label(pay_window, text="Scan to Pay", font=("Arial", 16, "bold")).pack(pady=10)
    tk.Label(pay_window, text=f"Amount Due: ₹{total_amount:.2f}", font=("Arial", 12)).pack(pady=5)
    
    # --- MOCK QR CODE GENERATOR ---
    # We use a Canvas to draw something that looks like a QR code without needing external libraries
    qr_canvas = tk.Canvas(pay_window, width=150, height=150, bg="white", highlightthickness=2, highlightbackground="black")
    
    # Draw the 3 big corner targeting squares
    for x, y in [(10, 10), (100, 10), (10, 100)]:
        qr_canvas.create_rectangle(x, y, x+40, y+40, fill="black")
        qr_canvas.create_rectangle(x+10, y+10, x+30, y+30, fill="white")
        qr_canvas.create_rectangle(x+15, y+15, x+25, y+25, fill="black")
        
    # Draw random small black blocks to simulate the QR pattern
    for _ in range(45):
        rx = random.randint(1, 14) * 10
        ry = random.randint(1, 14) * 10
        # Avoid drawing over our corner squares
        if not ((rx < 60 and ry < 60) or (rx > 90 and ry < 60) or (rx < 60 and ry > 90)):
            qr_canvas.create_rectangle(rx, ry, rx+10, ry+10, fill="black")
            
    qr_canvas.pack(pady=10)
    # ------------------------------
    
    tk.Label(pay_window, text="Use any UPI App (GPay, PhonePe, Paytm)", fg="gray", font=("Arial", 9)).pack()

    def process_success():
        """Finalizes the booking after simulated payment."""
        for idx in selected_seats:
            seat_status[idx] = 1
            buttons[idx].config(bg="red") # Turn buttons red permanently
        
        selected_seats.clear()
        messagebox.showinfo("Success", "Payment Received! Tickets have been sent to your email.")
        pay_window.destroy() # Close the payment window

    tk.Button(pay_window, text="Simulate Payment Complete", command=process_success, 
              bg="green", fg="white", font=("Arial", 11, "bold")).pack(pady=20)


# --- GUI Setup ---
root = tk.Tk()
root.title("Simple Movie Booking")
root.geometry("600x600")

lbl = tk.Label(root, text="Movie Ticket Booking", font=("Arial", 16, "bold"))
lbl.pack(pady=10)

# Combobox  
legend_frame = tk.Frame(root)
legend_frame.pack(pady=10)
cb = ttk.Combobox(legend_frame, values=movies, state="readonly")
cb.set(movies[0])
cb.bind("<<ComboboxSelected>>", selection_changed)
cb.pack(side=tk.LEFT, padx=5)

cb1 = ttk.Combobox(legend_frame, values=movielist[movies[0]][1], state="readonly")
cb1.current(0)
cb1.bind("<<ComboboxSelected>>", time_changed)
cb1.pack(side=tk.LEFT)


# Headers
lbl = tk.Label(root, text=movies[0], font=("Arial", 14, "bold"))
lbl.pack(pady=10)
pricelbl = tk.Label(root, text=f"Price: ₹{prices[0]}", font=("Arial", 10))
pricelbl.pack()

# Legend
legend_frame = tk.Frame(root)
legend_frame.pack(pady=10)
tk.Label(legend_frame, text="Available", bg="green", fg="white", width=8).pack(side=tk.LEFT, padx=2)
tk.Label(legend_frame, text="Booked", bg="red", fg="white", width=8).pack(side=tk.LEFT, padx=2)
tk.Label(root, text="SCREEN THIS WAY", bg="lightgray", width=40, font=("Arial", 10, "bold")).pack(pady=10)

# Seats Grid (2 rows of 5)
seat_frame = tk.Frame(root)
seat_frame.pack(pady=10)
showseats(movies[0], seat_frame)

# Book Button
tk.Button(root, text="Book Tickets", command=book_tickets, bg="orange", font=("Arial", 12, "bold")).pack(pady=20)

root.mainloop()
