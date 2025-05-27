import numpy as np
import pandas as pd
import gradio as gr
import time

# Load the flight data
df = pd.read_csv(r"C:\Users\jdaks\OneDrive\Desktop\mycodes\Python3.9\flight project\flight_records.csv", header=None)
df.columns = ["Flight name", "From", "To", "Seats", "Distance(kms)"]

# Clean and format
df["From"] = df["From"].str.strip().str.lower()
df["To"] = df["To"].str.strip().str.lower()
df = df[df["Seats"].apply(lambda x: str(x).isdigit())]
df = df[df["Distance(kms)"].apply(lambda x: str(x).isdigit())]
df["Seats"] = df["Seats"].astype(int)
df["Distance(kms)"] = df["Distance(kms)"].astype(int)

# Load the cost data
cost_df = pd.read_csv(r"C:\Users\jdaks\OneDrive\Desktop\mycodes\Python3.9\flight project\flight_basic_cost.csv", header=None)
cost_df.columns = ["airlines", "cost"]
cost_df["airlines"] = cost_df["airlines"].str.strip().str.lower()
cost_df["cost"] = cost_df["cost"].astype(int)

# Function to return available flights based on departure and destination
def get_available_flights(dept, dest):
    dept = dept.strip().lower()
    dest = dest.strip().lower()
    filtered_df = df[(df["From"] == dept) & (df["To"] == dest) & (df["Seats"] > 0)]
    
    if filtered_df.empty:
        return gr.update(choices=[], value=None), "❌ No flights found for this route."
    
    flight_options = list(filtered_df["Flight name"])
    info = "🛫 Available Flights:\n"
    for _, row in filtered_df.iterrows():
        info += f"{row['Flight name']} | Seats: {row['Seats']} | Distance: {row['Distance(kms)']} kms\n"
    
    return gr.update(choices=flight_options, value=flight_options[0]), info

# Booking function
def book_flight(dept, dest, flight_name, seat_count, food_choice, confirm):
    dept = dept.strip().lower()
    dest = dest.strip().lower()
    flight_name = flight_name.strip()

    if confirm != "y":
        return "❌ Booking not confirmed by user."

    filtered_df = df[(df["From"] == dept) & (df["To"] == dest)]
    selected_flight = filtered_df[filtered_df["Flight name"] == flight_name]

    if selected_flight.empty:
        return f"❌ No such flight '{flight_name}' found for this route."

    available_seats = int(selected_flight["Seats"].values[0])
    if seat_count > available_seats:
        return f"❌ Only {available_seats} seats available."

    distance = int(selected_flight["Distance(kms)"].values[0])
    airline_brand = flight_name.split()[0].strip().lower()
    cost_row = cost_df[cost_df["airlines"] == airline_brand]

    if cost_row.empty:
        return f"❌ Airline '{airline_brand}' cost not found."

    base_cost = int(cost_row["cost"].values[0])
    dist_cost = distance * 3
    food_cost = 500 if food_choice == 'y' else 0
    gst = 1000
    service_charge = 250
    single_seat_total = dist_cost + base_cost + food_cost + service_charge + gst
    total_cost = single_seat_total * seat_count

    # Update seat count
    flight_index = df[df["Flight name"] == flight_name].index[0]
    df.at[flight_index, "Seats"] -= seat_count
    df.to_csv(r"C:\Users\jdaks\OneDrive\Desktop\mycodes\Python3.9\flight project\flight_records.csv", index=False, header=False)

    return f"""✅ Seat booked successfully!
----------------------------------------
Flight Name       : {flight_name}
From              : {dept.title()}
To                : {dest.title()}
Distance (kms)    : {distance}
Seats Booked      : {seat_count}
----------------------------------------
Distance Cost     : Rs {dist_cost}
Airline Base Cost : Rs {base_cost}
Food Cost         : Rs {food_cost}
Service Charge    : Rs {service_charge}
GST               : Rs {gst}
----------------------------------------
Total Cost (1 seat): Rs {single_seat_total}
Total Cost ({seat_count} seats): Rs {total_cost}
----------------------------------------
🎉 Thank you! Visit Again."""

# Gradio UI
with gr.Blocks(title="Airline Booking System") as demo:
    gr.Markdown("## ✈️ Airline Reservation System")

    with gr.Row():
        dept = gr.Textbox(label="Departure City")
        dest = gr.Textbox(label="Destination City")
        check_btn = gr.Button("🔍 Show Flights")

    flight_dropdown = gr.Dropdown(choices=[], label="Select Flight")
    info_box = gr.Textbox(label="Flight Info", lines=4, interactive=False)

    seats = gr.Number(label="How Many Seats?", precision=0)
    food = gr.Radio(["y", "n"], label="Want Food?")
    confirm = gr.Radio(["y", "n"], label="Confirm Booking?")
    submit_btn = gr.Button("✅ Book Now")
    output = gr.Textbox(label="Booking Status", lines=10)

    check_btn.click(get_available_flights, inputs=[dept, dest], outputs=[flight_dropdown, info_box])
    submit_btn.click(book_flight, inputs=[dept, dest, flight_dropdown, seats, food, confirm], outputs=output)
    gr.HTML("""
<style>

  body {
    background: linear-gradient(to right, #e3f2fd, #ffffff);
    font-family: 'Segoe UI', sans-serif;
    background-color:black;
  }
  .gradio-container {
    max-width: 800px;
    margin: auto;
    border-radius: 10px;
    box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
    padding: 25px;
  }
  input, select, textarea {
    border-radius: 6px !important;
    padding: 10px !important;
    border: 1px solid #ccc !important;
  }
  button {
    background: linear-gradient(to right, #4e54c8, #8f94fb) !important;
    color: blue !important;
    font-weight: bold !important;
    border: none !important;
    padding: 12px 20px !important;
    border-radius: 6px !important;
  }
</style>
""")


demo.launch()
