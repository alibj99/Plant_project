import csv
import os
import uuid
from datetime import date, datetime, timedelta
from colorama import init, Fore, Back, Style


def read_csv(path):
    """
    Read csv and return all data.
    """
    data= []
    # Read CV and save data in dictionary
    with open(path, mode= 'r', newline='') as file:
        content = csv.DictReader(file)
        data = list(content)
        return data


def add_plant():
    """ Input all plant values """
    columns = ["ID", "Plant Name", "Location", "Date Acquired", "Watering Freq (days)", "Sunlight"]
    
    if not os.path.exists("Plants.csv") or not os.path.getsize("Plants.csv") > 0:
        with open("Plants.csv", "w", newline="", encoding="utf-8") as plants:
            Dictdata = csv.DictWriter(plants, fieldnames=columns)
            Dictdata.writeheader()

    # Add plant name (must be unique by name)
    while True:
        try:
            data = read_csv("Plants.csv")
            print(Fore.CYAN + "Please input the plant name/species:" + Style.RESET_ALL)
            p_name = input().strip()
            if p_name.lower() == "exit":
                return "Exited"
            if len(p_name) < 2:
                raise ValueError("Plant name must be at least 2 characters.")
            if any(x['Plant Name'].strip().lower() == p_name.lower() for x in data):
                raise Exception  # duplicate name
            break
        except ValueError as e:
            print(Fore.RED, e)
        except:
            print(Fore.RED + "This plant already exists in the system (same name).")

    # Add location
    while True:
        print(Fore.CYAN + "Please input the plant location (Living Room, Balcony, ....):" + Style.RESET_ALL)
        p_loc = input().strip()
        if p_loc.lower() == "exit":
            return "Exited"
        if len(p_loc) < 2:
            print(Fore.RED + "Location must be at least 2 characters.\n")
        else:
            break

    # Add Date Acquired 
    while True:
        try:
            print(Fore.CYAN + "Please input the Date Acquired in mm-dd-yyyy format:" + Style.RESET_ALL)
            new_date = input().strip()
            if new_date.lower() == "exit":
                return "Exited"
            formatted_date = datetime.strptime(new_date, "%m-%d-%Y")
            if formatted_date.date() > date.today():
                raise ValueError("Date Acquired cannot be in the future.")
            p_acq = formatted_date.strftime("%m-%d-%Y")
            break
        except ValueError:
            print(Fore.RED, f"Use MM-DD-YYYY format and try again.")

    # Add watering frequency (days)
    while True:
        try:
            print(Fore.CYAN + "Please input the watering frequency in days:" + Style.RESET_ALL)
            wf = input().strip()
            if wf.lower() == "exit":
                return "Exited"
            wf = int(wf)
            if wf < 1 :
                print(Fore.RED + "Please enter a valid number\n")
            else:
                break
        except ValueError:
            print(Fore.RED + "Incorrect value, please enter a number\n")

    # Add sunlight needs
    while True:
        try:
            print(
                Fore.CYAN
                + "Please input the sunlight needs: \n 1 for Low \n 2 for Medium \n 3 for High\n"
                + Style.RESET_ALL
            )
            s = input().strip()
            if s.lower() == "exit":
                return "Exited"
            s = int(s)
            if s < 1 or s > 3:
                raise ValueError
            if s == 1:
                sunlight = "Low"
            elif s == 2:
                sunlight = "Medium"
            elif s == 3:
                sunlight = "High"
            break
        except ValueError:
            print(Fore.RED + "Incorrect value, please try again\n")

    # Generate simple ID
    try:
        existing = read_csv("Plants.csv")
        next_num = len(existing) + 1
    except:
        next_num = 1
    pid = next_num

    # Write row
    with open("Plants.csv", "a", newline="", encoding="utf-8") as plants:
        Dictdata = csv.DictWriter(plants, fieldnames=columns)
        Dictdata.writerow(
            {
                "ID": pid,
                "Plant Name": p_name,
                "Location": p_loc,
                "Date Acquired": p_acq,
                "Watering Freq (days)": wf,
                "Sunlight": sunlight,
            }
        )
        print(Fore.BLUE + "Plant has been added successfully." + Style.RESET_ALL)

    
def record_care_activity():
    """
    Entering the activity
    """
    path = "Plants.csv"
    base_cols = ["ID","Plant Name","Location","Date Acquired","Watering Freq (days)","Sunlight"]
    care_cols = ["Watering Date","Fertilizing Date","Repotting Date","Pruning Date"]
    all_cols  = base_cols + care_cols

    if not os.path.exists(path) or not os.path.getsize(path) > 0:
        print(Fore.RED + "No plants found. Please add a plant first.")
        return "Exited"

    try:
        rows = read_csv(path)
    except FileNotFoundError:
        print(Fore.RED + "Plants.csv not found.")
        return "Exited"

    # make sure care columns exist
    for r in rows:
        for c in care_cols:
            r.setdefault(c, "")

    # pick plant
    while True:
        print(Fore.CYAN + "Enter Plant Name or Plant ID (or 'exit'):" + Style.RESET_ALL)
        sel = input().strip()
        if sel.lower() == "exit":
            return "Exited"
        plant = next((r for r in rows
                      if r.get("ID","") == sel
                      or r.get("Plant Name","").strip().lower() == sel.strip().lower()), None)
        if plant:
            break
        print(Fore.RED + "No matching plant. Try again.")

    # pick activity
    map_num = {"1":"Watering","2":"Fertilizing","3":"Repotting","4":"Pruning"}
    map_txt = {k.lower(): v for k, v in map_num.items()}
    while True:
        print(Fore.CYAN + "Choose Activity: 1 Watering | 2 Fertilizing | 3 Repotting | 4 Pruning (or 'exit')" + Style.RESET_ALL)
        a = input().strip().lower()
        if a == "exit":
            return "Exited"
        activity = map_num.get(a) or map_txt.get(a)
        if activity:
            break
        print(Fore.RED + "Invalid activity. Try again.")

    # overwrite date for the chosen activity
    today_str  = date.today().strftime("%m-%d-%Y")
    target_col = f"{activity} Date"
    for r in rows:
        if r["ID"] == plant["ID"]:
            r[target_col] = today_str
            break

    # rewrite file
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=all_cols)
        w.writeheader()
        w.writerows(rows)

    print(Fore.BLUE + f"{activity} recorded for '{plant['Plant Name']}' on {today_str}." + Style.RESET_ALL)


def view_plants_due_for_care():
    """List plants that need attention (watering + other activities)."""
    try:
        rows = read_csv("Plants.csv")
    except FileNotFoundError:
        print("No plants found."); return "Exited"
    if not rows:
        print("No plants found."); return "Exited"

    INTERVALS = {"Fertilizing Date": 30, "Repotting Date": 365, "Pruning Date": 90}  # watering uses freq
    today = date.today()
    any_due = False

    print("\n=== Plants Due for Care ===")
    for r in rows:
        name = (r.get("Plant Name") or "(Unnamed)").strip()
        pid  = (r.get("ID") or "").strip()

        # watering frequency (default 7 if missing/invalid)
        try:
            freq = int((r.get("Watering Freq (days)") or "7").strip())
        except:
            freq = 7

        # last watering
        s_w = (r.get("Watering Date") or "").strip()
        try:
            last_w = datetime.strptime(s_w, "%m-%d-%Y").date() if s_w else None
        except:
            last_w = None

        watering_due = (last_w is None) or (last_w + timedelta(days=freq) <= today)

        # other attention (due if empty OR last + interval <= today)
        needs = []
        for col, days in INTERVALS.items():
            s_a = (r.get(col) or "").strip()
            try:
                last_a = datetime.strptime(s_a, "%m-%d-%Y").date() if s_a else None
            except:
                last_a = None
            if (last_a is None) or (last_a + timedelta(days=days) <= today):
                needs.append(col.replace(" Date", ""))

        # output
        if watering_due or needs:
            any_due = True
            last_w_str = last_w.strftime("%m-%d-%Y") if last_w else "Unknown"
            line = f"- {name} [{pid}]"
            if watering_due:
                line += f" • Watering due (every {freq}d you have to do watering, last watering day: {last_w_str})"
            print(line)
            if needs:
                print("  • Needs: " + ", ".join(needs))

    if not any_due:
        print("All good! Nothing due today.")




def search_plants():
    """Search plants by name or location and display last activity dates."""
    plants = read_csv("Plants.csv")
    if not plants:
        print("No plants to search.")
        return "Exited"

    print("Search term (name or location) or 'exit':\n")
    term = input("Search term (name or location) or 'exit': ").strip().lower()
    if term == "exit":
        return "Exited"

    # make sure activity columns exist in memory
    for p in plants:
        p.setdefault("Watering Date", "")
        p.setdefault("Fertilizing Date", "")
        p.setdefault("Repotting Date", "")
        p.setdefault("Pruning Date", "")

    results = [
        p for p in plants
        if term in p.get("Plant Name","").lower() or term in p.get("Location","").lower()
    ]
    if not results:
        print("No matches.")
        return

    for p in results:
        print(f"- {p['Plant Name']} [{p['ID']}] • {p['Location']} • Acquired {p['Date Acquired']} "
              f"• Water every {p['Watering Freq (days)']}d • Sun {p.get('Sunlight','')}")
        print(f"  Activities -> Watering: {p['Watering Date'] or '-'}, "
              f"Fertilizing: {p['Fertilizing Date'] or '-'}, "
              f"Repotting: {p['Repotting Date'] or '-'}, "
              f"Pruning: {p['Pruning Date'] or '-'}")

def view_all_plants():
    """Display all plants (minimal)."""
    try:
        rows = read_csv("Plants.csv")
    except FileNotFoundError:
        print("No plants found."); return "Exited"
    if not rows:
        print("No plants found."); return "Exited"
    for p in rows:
        print(f"- {p.get('Plant Name','(Unnamed)')} [{p.get('ID','')}] • {p.get('Location','')} • Acquired {p.get('Date Acquired','')} • Every {p.get('Watering Freq (days)','?')}d • Sun {p.get('Sunlight','')}")

# ---------- menu + main ----------
def display_menu():
    """Display the main menu options."""
    print("\n=== Plant Care Tracker ===")
    print("1. Add a new plant to the collection")
    print("2. Record a plant care activity")
    print("3. View plants due for care")
    print("4. Search plants")
    print("5. View all plants")
    print("6. Exit")
    return input("Enter your choice (1-6): ").strip()

def main():
    """Main application function."""
    print("Welcome to Plant Care Tracker!")
    while True:
        choice = display_menu()
        ret = None
        if choice == '1':
            ret = add_plant()
        elif choice == '2':
            ret = record_care_activity()
        elif choice == '3':
            ret = view_plants_due_for_care()
        elif choice == '4':
            ret = search_plants()
        elif choice == '5':
            ret = view_all_plants()
        elif choice == '6':
            print("Thank you for using Plant Care Tracker. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 6.")
            continue

        # If a function returns "Exited", just show the menu again
        if ret == "Exited":
            continue