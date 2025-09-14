🌱 Plant Care Tracker

The Plant Care Tracker is a simple Python-based tool that helps you monitor and manage the care schedule of your plants. It reads plant data from a CSV file and identifies which plants are due for watering, fertilizing, pruning, or repotting.

📋 Features

Reads plant data from a CSV file (Plants.csv).

Tracks multiple care activities:

🌊 Watering (based on frequency in days).

🌱 Fertilizing (default: every 30 days).

✂️ Pruning (default: every 90 days).

🪴 Repotting (default: every 365 days).

Compares the last recorded care date with today’s date.

Outputs a clear list of plants that need attention.


Run the tracker:

python plant_tracker.py


Example output:

=== Plants Due for Care ===
🌊 Watering: Aloe Vera (ID: 005)
🌱 Fertilizing: Rose (ID: 001)
🪴 Repotting: Snake Plant (ID: 003)

⚙️ Configuration

You can adjust the care intervals inside plant_tracker.py:

INTERVALS = {
    "Fertilizing Date": 30,
    "Repotting Date": 365,
    "Pruning Date": 90
}

📌 Future Improvements

Add a notification system (email or push notifications).

Track plant growth notes and images.

GUI version for easier use.
