import pandas as pd
from faker import Faker
import random
from datetime import datetime, timedelta

# Initialize Faker for Saudi Arabia
fake = Faker('ar_SA')

# --- Configuration ---
NUM_ROWS = 75
OUTPUT_CSV_FILE = 'travel_agency_dataset.csv'

# --- Data Options ---
DESTINATIONS = [
    "Dubai, UAE", "Istanbul, Turkey", "Mecca, Saudi Arabia", "Medina, Saudi Arabia",
    "Paris, France", "Kuala Lumpur, Malaysia", "London, UK", "Cairo, Egypt",
    "Jeddah, Saudi Arabia", "Riyadh, Saudi Arabia", "Dammam, Saudi Arabia",
    "Abha, Saudi Arabia", "AlUla, Saudi Arabia", "NEOM, Saudi Arabia"
]

PACKAGE_TYPES = ["Luxury", "Budget", "Adventure", "Religious", "Business", "Family"]
PAYMENT_STATUSES = ["Paid", "Pending", "Cancelled"]
AGENT_NAMES = ["Ahmed Khan", "Fatima Al-Jameel", "Mohammed Al-Zahrani", "Noura Al-Mutairi", "Khalid Al-Ghamdi"]
BOOKING_CHANNELS = ["Walk-in", "Website", "WhatsApp", "Referral"]
SPECIAL_REQUESTS_OPTIONS = ["Wheelchair access", "Halal meals", "Private tour guide", "Sea view room", "Extra luggage", ""]

# --- Helper Functions ---
def generate_booking_id():
    """Generates a unique alphanumeric booking ID."""
    return f"SA{random.randint(10000, 99999)}{random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')}"

def generate_dates():
    """Generates realistic departure and return dates."""
    departure_date = datetime.now() + timedelta(days=random.randint(-30, 180))
    trip_duration = timedelta(days=random.randint(3, 15))
    return_date = departure_date + trip_duration
    return departure_date.strftime("%d/%m/%Y"), return_date.strftime("%d/%m/%Y")

def get_realistic_cost(package_type, destination):
    """Generates a realistic cost based on package and destination."""
    base_cost = {
        "Luxury": 5000, "Business": 4000, "Family": 3500,
        "Adventure": 3000, "Religious": 2500, "Budget": 1500
    }
    cost = base_cost.get(package_type, 2000)

    # Increase cost for international destinations
    if "Saudi Arabia" not in destination:
        cost *= 1.5

    # Add random variation
    cost += random.randint(-500, 500)
    return round(cost, 2)

# --- Main Data Generation ---
data = []
for _ in range(NUM_ROWS):
    package_type = random.choice(PACKAGE_TYPES)
    destination = random.choice(DESTINATIONS)

    # Ensure religious packages are for Mecca/Medina
    if package_type == "Religious":
        destination = random.choice(["Mecca, Saudi Arabia", "Medina, Saudi Arabia"])

    departure_date, return_date = generate_dates()
    total_cost = get_realistic_cost(package_type, destination)
    payment_status = random.choice(PAYMENT_STATUSES)

    # If cancelled, cost should be adjusted or noted (optional, for simplicity we keep it)
    if payment_status == "Cancelled":
         # Often a cancellation fee or partial payment is made
        total_cost = total_cost * random.uniform(0.1, 0.3)


    row = {
        "Booking ID": generate_booking_id(),
        "Client Name (English)": fake.name(),
        "Client Name (Arabic)": fake.name_male() if random.choice([True, False]) else fake.name_female(),
        "Destination": destination,
        "Package Type": package_type,
        "Departure Date": departure_date,
        "Return Date": return_date,
        "Total Cost (SAR)": f"{total_cost:,.2f}",
        "Payment Status": payment_status,
        "Agent Name": random.choice(AGENT_NAMES),
        "Booking Channel": random.choice(BOOKING_CHANNELS),
        "Client Rating (1-5 stars)": random.randint(1, 5) if payment_status == "Paid" else "",
        "Special Requests": random.choice(SPECIAL_REQUESTS_OPTIONS)
    }
    data.append(row)

# --- Create and Save DataFrame ---
df = pd.DataFrame(data)

# Reorder columns to match request
df = df[[
    "Booking ID", "Client Name (English)", "Client Name (Arabic)", "Destination",
    "Package Type", "Departure Date", "Return Date", "Total Cost (SAR)",
    "Payment Status", "Agent Name", "Booking Channel", "Client Rating (1-5 stars)",
    "Special Requests"
]]

df.to_csv(OUTPUT_CSV_FILE, index=False, encoding='utf-8-sig')

print(f"Successfully generated {NUM_ROWS} rows of data in '{OUTPUT_CSV_FILE}'")
