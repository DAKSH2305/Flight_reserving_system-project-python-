

import numpy as np 
import pandas as pd 
import gradio as gr
import time



# Load CSV
df = pd.read_csv(r"C:\Users\jdaks\OneDrive\Desktop\mycodes\Python3.9\flight project\flight_records.csv", header=None)
df.columns = ["Flight name", "From", "To", "Seats", "Distance(kms)"]
df["From"] = df["From"].str.strip().str.lower()
df["To"] = df["To"].str.strip().str.lower()

# Class definition
class flight_details:
    def __init__(self, dept, dest):
        self.From = dept.strip().lower()
        self.to = dest.strip().lower()
        
        
    def selection(self):
        print()
        fl_name=input("enter flight name : ")
        seat=int(input("how many seats : "))
        newdf=df[df["Flight name"]==fl_name]
        distance=newdf["Distance(kms)"].values[0]
        time.sleep(1.5)
        if newdf.empty:
            print("No such flight found for this route")
            return None, None, None, None
        else:
            time.sleep(1)
            available_seats = int(newdf["Seats"].values[0])

            if(seat<=available_seats):
                print(f" Available {available_seats} ")
                print()
                print()
                time.sleep(1)
            
                confirm=input("confirm booking in this (y/n) : ")
                return confirm,distance,newdf["Flight name"].values[0],seat
            
            else:
                print("Not enough seats available")
                return None, None, None, None
            
        
    def allotment(self):
        confirmation,distan,aircraft,nseats=self.selection()
        cost_df = pd.read_csv(r"C:\Users\jdaks\OneDrive\Desktop\mycodes\Python3.9\flight project\flight_basic_cost.csv", header=None)

        cost_df.columns = ["airlines", "cost"]
        cost_df["airlines"] = cost_df["airlines"].str.strip().str.lower()

        
        cost=0
        if confirmation != "y" or not all([distan, aircraft, nseats]):
            print("❌ Booking not confirmed or invalid flight.")
            print()
            time.sleep(2)
            print("Thank You . Visit Again")
            return
        else:
            food_choice= 500 if(input("would like to purchase food for your journey (y/n) :")=='y') else 0
            print()
            print()
            dist_cost=distan*3  # i am here 
            airline_brand = aircraft.split()[0].strip().lower()



            matched_row = cost_df[cost_df["airlines"] == airline_brand]
            if matched_row.empty:
                print("❌ Airline not found in database.")
                return


            base_cost = matched_row["cost"].values[0]
            total=food_choice+250+base_cost+dist_cost
            time.sleep(1)
            print("seat booked successfully !!!")
            print("")
            time.sleep(1.5)
            print(" Ticket fare : Rs" ,dist_cost)
            
            print("airline company basic cost : Rs",matched_row["cost"].values[0])
            print("food cost : Rs",food_choice)
            print("GST : Rs",1000)
            print(f"total cost : Rs ",1000+ total,f"x {nseats} = Rs",(total+1000)*nseats)
            print()
            time.sleep(1)
            print("Thank You . Visit Again")
            # --- Update seats in main DataFrame and save ---
            flight_index = df[df["Flight name"] == aircraft].index[0]
            
           
            df.at[flight_index, "Seats"] =int(df.at[flight_index, "Seats"] )- nseats 
            
            
# Save back to CSV
            df.to_csv(r"C:\Users\jdaks\OneDrive\Desktop\mycodes\Python3.9\flight project\flight_records.csv", index=False, header=False)


        
        

    def display_flights(self):
        filtered_df = df[(df["From"] == self.From) & (df["To"] == self.to)]
        if filtered_df.empty:
            print()
            print("No flights found for this route") 
            print("Thank You . Visit Again")
            return False
        else:
            print()
            print("*************************************")
            print(filtered_df)
            print("*************************************")
            time.sleep(1)
            print("                    || choose flight ||")
            print()
            return True
        
print()
print("!! WELCOME TO OUR AIRLINES RESERVATION PLATFORM !!")
print("*************************************************")
time.sleep(1.5)

dep=input("departure city : ")
des=input("destination city : ")
time.sleep(1.5)
f1=flight_details(dep,des)
work=f1.display_flights()

if(work):
    f1.allotment()


