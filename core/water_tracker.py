import datetime
import json
import os
import calendar
from typing import Dict, List, Tuple, Optional

WATER_LOG_FILE = 'water_intake_log.json'

# Helper to get today's date as string
def today_str():
    """
    Get today's date as ISO format string.
    Returns:
        str: Today's date in YYYY-MM-DD format.
    """
    return datetime.date.today().isoformat()


# Log water intake (in ml)
def log_water_intake(amount_ml):
    """
    Log water intake for the current day.
    Args:
        amount_ml (int/float): Amount of water in milliliters.
    """
    data = load_water_log()
    today = today_str()
    if today not in data:
        data[today] = []
    data[today].append({
        'amount_ml': amount_ml, 
        'timestamp': datetime.datetime.now().isoformat()
    })
    save_water_log(data)


def log_water_intake_with_note(amount_ml, note=""):
    """
    Log water intake with an optional note/description.
    Args:
        amount_ml (int/float): Amount of water in milliliters.
        note (str): Optional note about the intake (e.g., "After workout", "Morning").
    """
    data = load_water_log()
    today = today_str()
    if today not in data:
        data[today] = []
    data[today].append({
        'amount_ml': amount_ml,
        'timestamp': datetime.datetime.now().isoformat(),
        'note': note
    })
    save_water_log(data)


def log_water_intake_for_date(amount_ml, date_str, note=""):
    """
    Log water intake for a specific date (useful for backdating entries).
    Args:
        amount_ml (int/float): Amount of water in milliliters.
        date_str (str): Date in YYYY-MM-DD format.
        note (str): Optional note about the intake.
    Returns:
        bool: True if successful, False otherwise.
    """
    try:
        # Validate date format
        datetime.date.fromisoformat(date_str)
        
        data = load_water_log()
        if date_str not in data:
            data[date_str] = []
        data[date_str].append({
            'amount_ml': amount_ml,
            'timestamp': datetime.datetime.now().isoformat(),
            'note': note
        })
        save_water_log(data)
        return True
    except ValueError:
        return False


# Get total water intake for today (in ml)
def get_today_total():
    """
    Get total water intake for today in milliliters.
    Returns:
        int: Total water intake in ml.
    """
    data = load_water_log()
    today = today_str()
    if today in data:
        return sum(entry['amount_ml'] for entry in data[today])
    return 0


def get_total_for_date(date_str):
    """
    Get total water intake for a specific date.
    Args:
        date_str (str): Date in YYYY-MM-DD format.
    Returns:
        int: Total water intake in ml for that date.
    """
    data = load_water_log()
    if date_str in data:
        return sum(entry['amount_ml'] for entry in data[date_str])
    return 0


def get_average_daily_intake(days=7):
    """
    Calculate average daily water intake over the last N days.
    Args:
        days (int): Number of days to calculate average for.
    Returns:
        float: Average daily intake in ml.
    """
    totals = get_last_n_days_totals(days)
    if not totals:
        return 0.0
    total_intake = sum(total for _, total in totals)
    return round(total_intake / len(totals), 2)


def get_hydration_percentage(daily_goal_ml=2000):
    """
    Get today's hydration as a percentage of daily goal.
    Args:
        daily_goal_ml (int): Daily water intake goal in ml.
    Returns:
        float: Percentage of goal achieved (0-100+).
    """
    today_total = get_today_total()
    return round((today_total / daily_goal_ml) * 100, 1) if daily_goal_ml > 0 else 0


def is_goal_achieved(daily_goal_ml=2000):
    """
    Check if today's water intake goal has been achieved.
    Args:
        daily_goal_ml (int): Daily water intake goal in ml.
    Returns:
        bool: True if goal achieved, False otherwise.
    """
    return get_today_total() >= daily_goal_ml


# Load water log from file
def load_water_log():
    """
    Load water log data from JSON file.
    Returns:
        dict: Water log data with dates as keys.
    """
    if not os.path.exists(WATER_LOG_FILE):
        return {}
    with open(WATER_LOG_FILE, 'r') as f:
        return json.load(f)


# Save water log to file
def save_water_log(data):
    """
    Save water log data to JSON file.
    Args:
        data (dict): Water log data to save.
    """
    with open(WATER_LOG_FILE, 'w') as f:
        json.dump(data, f, indent=2)


def backup_water_log():
    """
    Create a backup of the water log file with timestamp.
    Returns:
        str: Path to backup file, or None if backup failed.
    """
    try:
        if not os.path.exists(WATER_LOG_FILE):
            return None
        
        backup_dir = 'backups'
        os.makedirs(backup_dir, exist_ok=True)
        
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_file = f'{backup_dir}/water_log_backup_{timestamp}.json'
        
        data = load_water_log()
        with open(backup_file, 'w') as f:
            json.dump(data, f, indent=2)
        
        return backup_file
    except Exception as e:
        print(f"Backup failed: {e}")
        return None


# Get all water intake entries for today
def get_today_entries():
    """
    Get all water intake entries for today.
    Returns:
        list: List of entry dictionaries for today.
    """
    data = load_water_log()
    today = today_str()
    return data.get(today, [])


def get_entries_for_date(date_str):
    """
    Get all water intake entries for a specific date.
    Args:
        date_str (str): Date in YYYY-MM-DD format.
    Returns:
        list: List of entry dictionaries for that date.
    """
    data = load_water_log()
    return data.get(date_str, [])


# Delete a specific water intake entry by its timestamp
def delete_water_intake_entry(timestamp):
    """
    Delete a specific water intake entry by timestamp.
    Args:
        timestamp (str): ISO format timestamp of the entry to delete.
    Returns:
        bool: True if deleted successfully, False otherwise.
    """
    data = load_water_log()
    today = today_str()
    if today in data:
        original_count = len(data[today])
        data[today] = [entry for entry in data[today] if entry['timestamp'] != timestamp]
        
        if len(data[today]) < original_count:
            save_water_log(data)
            return True
    return False


def delete_entry_for_date(date_str, timestamp):
    """
    Delete a water intake entry for a specific date by timestamp.
    Args:
        date_str (str): Date in YYYY-MM-DD format.
        timestamp (str): ISO format timestamp of the entry to delete.
    Returns:
        bool: True if deleted successfully, False otherwise.
    """
    data = load_water_log()
    if date_str in data:
        original_count = len(data[date_str])
        data[date_str] = [entry for entry in data[date_str] if entry['timestamp'] != timestamp]
        
        if len(data[date_str]) < original_count:
            save_water_log(data)
            return True
    return False


def delete_all_entries_for_date(date_str):
    """
    Delete all water intake entries for a specific date.
    Args:
        date_str (str): Date in YYYY-MM-DD format.
    Returns:
        bool: True if deleted successfully, False if date not found.
    """
    data = load_water_log()
    if date_str in data:
        del data[date_str]
        save_water_log(data)
        return True
    return False


# Get water intake data for a specific month
def get_monthly_data(year, month):
    """
    Get water intake totals for each day in a specific month.
    Args:
        year (int): Year (e.g., 2025).
        month (int): Month (1-12).
    Returns:
        dict: Dictionary with date strings as keys and totals (ml) as values.
    """
    data = load_water_log()
    month_data = {}
    num_days = calendar.monthrange(year, month)[1]
    for day in range(1, num_days + 1):
        date_str = f"{year}-{month:02d}-{day:02d}"
        total = sum(entry['amount_ml'] for entry in data.get(date_str, []))
        month_data[date_str] = total
    return month_data


def get_monthly_statistics(year, month):
    """
    Get comprehensive statistics for a specific month.
    Args:
        year (int): Year (e.g., 2025).
        month (int): Month (1-12).
    Returns:
        dict: Statistics including total, average, best/worst days.
    """
    month_data = get_monthly_data(year, month)
    totals = [amount for amount in month_data.values() if amount > 0]
    
    if not totals:
        return {
            'total': 0,
            'average': 0,
            'best_day': None,
            'worst_day': None,
            'days_logged': 0
        }
    
    best_date = max(month_data.items(), key=lambda x: x[1])
    worst_date = min((item for item in month_data.items() if item[1] > 0), key=lambda x: x[1])
    
    return {
        'total': sum(totals),
        'average': round(sum(totals) / len(totals), 2),
        'best_day': {'date': best_date[0], 'amount': best_date[1]},
        'worst_day': {'date': worst_date[0], 'amount': worst_date[1]},
        'days_logged': len(totals),
        'days_in_month': len(month_data)
    }


# Edit a specific water intake entry
def edit_water_intake_entry(timestamp, new_amount_ml):
    """
    Edit the amount of a specific water intake entry.
    Args:
        timestamp (str): ISO format timestamp of the entry to edit.
        new_amount_ml (int/float): New amount in milliliters.
    Returns:
        bool: True if edited successfully, False otherwise.
    """
    data = load_water_log()
    today = today_str()
    if today in data:
        for entry in data[today]:
            if entry['timestamp'] == timestamp:
                entry['amount_ml'] = new_amount_ml
                save_water_log(data)
                return True
    return False


def edit_entry_for_date(date_str, timestamp, new_amount_ml, new_note=None):
    """
    Edit a water intake entry for a specific date.
    Args:
        date_str (str): Date in YYYY-MM-DD format.
        timestamp (str): ISO format timestamp of the entry to edit.
        new_amount_ml (int/float): New amount in milliliters.
        new_note (str, optional): New note for the entry.
    Returns:
        bool: True if edited successfully, False otherwise.
    """
    data = load_water_log()
    if date_str in data:
        for entry in data[date_str]:
            if entry['timestamp'] == timestamp:
                entry['amount_ml'] = new_amount_ml
                if new_note is not None:
                    entry['note'] = new_note
                save_water_log(data)
                return True
    return False


# Get water intake totals for the last N days (returns list of (date, total_ml))
def get_last_n_days_totals(n=7):
    """
    Get water intake totals for the last N days.
    Args:
        n (int): Number of days to retrieve.
    Returns:
        list: List of tuples (date_str, total_ml) for the last N days.
    """
    data = load_water_log()
    today = datetime.date.today()
    days = [(today - datetime.timedelta(days=i)).isoformat() for i in range(n-1, -1, -1)]
    return [(d, sum(e['amount_ml'] for e in data.get(d, []))) for d in days]


def get_streak_count(daily_goal_ml=2000):
    """
    Get current streak of consecutive days meeting the daily goal.
    Args:
        daily_goal_ml (int): Daily water intake goal in ml.
    Returns:
        int: Number of consecutive days meeting goal (including today).
    """
    data = load_water_log()
    today = datetime.date.today()
    streak = 0
    
    for i in range(365):  # Check up to 1 year back
        date_str = (today - datetime.timedelta(days=i)).isoformat()
        daily_total = sum(entry['amount_ml'] for entry in data.get(date_str, []))
        
        if daily_total >= daily_goal_ml:
            streak += 1
        else:
            break
    
    return streak


def get_longest_streak(daily_goal_ml=2000):
    """
    Get the longest streak of consecutive days meeting the daily goal.
    Args:
        daily_goal_ml (int): Daily water intake goal in ml.
    Returns:
        dict: Dictionary with 'length', 'start_date', and 'end_date'.
    """
    data = load_water_log()
    if not data:
        return {'length': 0, 'start_date': None, 'end_date': None}
    
    # Get all dates sorted
    sorted_dates = sorted(data.keys())
    
    max_streak = 0
    current_streak = 0
    streak_start = None
    max_streak_start = None
    max_streak_end = None
    
    for date_str in sorted_dates:
        daily_total = sum(entry['amount_ml'] for entry in data.get(date_str, []))
        
        if daily_total >= daily_goal_ml:
            if current_streak == 0:
                streak_start = date_str
            current_streak += 1
            
            if current_streak > max_streak:
                max_streak = current_streak
                max_streak_start = streak_start
                max_streak_end = date_str
        else:
            current_streak = 0
            streak_start = None
    
    return {
        'length': max_streak,
        'start_date': max_streak_start,
        'end_date': max_streak_end
    }


def get_weekly_summary():
    """
    Get a summary of the current week's water intake.
    Returns:
        dict: Weekly statistics including total, average, and daily breakdown.
    """
    data = get_last_n_days_totals(7)
    totals = [amount for _, amount in data]
    
    return {
        'total': sum(totals),
        'average': round(sum(totals) / 7, 2),
        'daily_breakdown': data,
        'days_with_intake': sum(1 for amount in totals if amount > 0),
        'best_day': max(data, key=lambda x: x[1]) if totals else None,
        'worst_day': min(data, key=lambda x: x[1]) if totals else None
    }


def get_all_time_statistics():
    """
    Get all-time statistics for water intake.
    Returns:
        dict: Comprehensive statistics including total days, total intake, etc.
    """
    data = load_water_log()
    
    if not data:
        return {
            'total_days_logged': 0,
            'total_intake': 0,
            'average_per_day': 0,
            'best_day': None,
            'total_entries': 0
        }
    
    all_totals = []
    total_entries = 0
    
    for date_str, entries in data.items():
        daily_total = sum(entry['amount_ml'] for entry in entries)
        if daily_total > 0:
            all_totals.append((date_str, daily_total))
        total_entries += len(entries)
    
    if not all_totals:
        return {
            'total_days_logged': 0,
            'total_intake': 0,
            'average_per_day': 0,
            'best_day': None,
            'total_entries': 0
        }
    
    best_day = max(all_totals, key=lambda x: x[1])
    
    return {
        'total_days_logged': len(all_totals),
        'total_intake': sum(amount for _, amount in all_totals),
        'average_per_day': round(sum(amount for _, amount in all_totals) / len(all_totals), 2),
        'best_day': {'date': best_day[0], 'amount': best_day[1]},
        'total_entries': total_entries,
        'first_logged_date': min(data.keys()),
        'last_logged_date': max(data.keys())
    }


def convert_ml_to_liters(ml):
    """
    Convert milliliters to liters.
    Args:
        ml (int/float): Amount in milliliters.
    Returns:
        float: Amount in liters, rounded to 2 decimal places.
    """
    return round(ml / 1000, 2)


def convert_liters_to_ml(liters):
    """
    Convert liters to milliliters.
    Args:
        liters (int/float): Amount in liters.
    Returns:
        int: Amount in milliliters.
    """
    return int(liters * 1000)


def convert_ml_to_cups(ml, cup_size_ml=250):
    """
    Convert milliliters to cups.
    Args:
        ml (int/float): Amount in milliliters.
        cup_size_ml (int): Size of one cup in ml (default 250ml).
    Returns:
        float: Number of cups, rounded to 1 decimal place.
    """
    return round(ml / cup_size_ml, 1)


def get_hydration_reminder_times(wake_time="07:00", sleep_time="23:00", interval_hours=2):
    """
    Generate suggested reminder times for water intake throughout the day.
    Args:
        wake_time (str): Wake time in HH:MM format.
        sleep_time (str): Sleep time in HH:MM format.
        interval_hours (int): Hours between reminders.
    Returns:
        list: List of time strings in HH:MM format.
    """
    wake_hour, wake_min = map(int, wake_time.split(':'))
    sleep_hour, sleep_min = map(int, sleep_time.split(':'))
    
    wake_dt = datetime.datetime.combine(datetime.date.today(), datetime.time(wake_hour, wake_min))
    sleep_dt = datetime.datetime.combine(datetime.date.today(), datetime.time(sleep_hour, sleep_min))
    
    reminders = []
    current_time = wake_dt
    
    while current_time < sleep_dt:
        reminders.append(current_time.strftime("%H:%M"))
        current_time += datetime.timedelta(hours=interval_hours)
    
    return reminders


def export_data_to_csv(output_file='water_intake_export.csv'):
    """
    Export all water intake data to a CSV file.
    Args:
        output_file (str): Path to the output CSV file.
    Returns:
        bool: True if export successful, False otherwise.
    """
    try:
        import csv
        data = load_water_log()
        
        with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Date', 'Timestamp', 'Amount (ml)', 'Note'])
            
            for date_str in sorted(data.keys()):
                for entry in data[date_str]:
                    writer.writerow([
                        date_str,
                        entry.get('timestamp', ''),
                        entry.get('amount_ml', 0),
                        entry.get('note', '')
                    ])
        
        return True
    except Exception as e:
        print(f"Export failed: {e}")
        return False


def import_data_from_csv(input_file='water_intake_export.csv'):
    """
    Import water intake data from a CSV file.
    Args:
        input_file (str): Path to the input CSV file.
    Returns:
        bool: True if import successful, False otherwise.
    """
    try:
        import csv
        data = load_water_log()
        
        with open(input_file, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            
            for row in reader:
                date_str = row['Date']
                if date_str not in data:
                    data[date_str] = []
                
                data[date_str].append({
                    'amount_ml': float(row['Amount (ml)']),
                    'timestamp': row['Timestamp'],
                    'note': row.get('Note', '')
                })
        
        save_water_log(data)
        return True
    except Exception as e:
        print(f"Import failed: {e}")
        return False


def calculate_recommended_intake(weight_kg=70, activity_level='moderate', climate='temperate'):
    """
    Calculate recommended daily water intake based on personal factors.
    Args:
        weight_kg (float): Body weight in kilograms.
        activity_level (str): 'sedentary', 'moderate', or 'active'.
        climate (str): 'cold', 'temperate', or 'hot'.
    Returns:
        int: Recommended daily intake in milliliters.
    """
    # Base calculation: 30-35ml per kg of body weight
    base_intake = weight_kg * 33
    
    # Adjust for activity level
    activity_multipliers = {
        'sedentary': 1.0,
        'moderate': 1.15,
        'active': 1.3
    }
    base_intake *= activity_multipliers.get(activity_level, 1.0)
    
    # Adjust for climate
    climate_additions = {
        'cold': 0,
        'temperate': 200,
        'hot': 500
    }
    base_intake += climate_additions.get(climate, 200)
    
    return int(base_intake)


def get_intake_by_time_of_day():
    """
    Get water intake breakdown by time of day (morning, afternoon, evening, night).
    Returns:
        dict: Water intake totals for each time period.
    """
    entries = get_today_entries()
    
    periods = {
        'morning': 0,    # 5am - 12pm
        'afternoon': 0,  # 12pm - 5pm
        'evening': 0,    # 5pm - 9pm
        'night': 0       # 9pm - 5am
    }
    
    for entry in entries:
        try:
            timestamp = datetime.datetime.fromisoformat(entry['timestamp'])
            hour = timestamp.hour
            
            if 5 <= hour < 12:
                periods['morning'] += entry['amount_ml']
            elif 12 <= hour < 17:
                periods['afternoon'] += entry['amount_ml']
            elif 17 <= hour < 21:
                periods['evening'] += entry['amount_ml']
            else:
                periods['night'] += entry['amount_ml']
        except:
            continue
    
    return periods


def clear_old_data(days_to_keep=90):
    """
    Delete water intake data older than specified days.
    Args:
        days_to_keep (int): Number of days of data to retain.
    Returns:
        int: Number of days deleted.
    """
    data = load_water_log()
    cutoff_date = (datetime.date.today() - datetime.timedelta(days=days_to_keep)).isoformat()
    
    dates_to_delete = [date for date in data.keys() if date < cutoff_date]
    
    for date in dates_to_delete:
        del data[date]
    
    if dates_to_delete:
        save_water_log(data)
    
    return len(dates_to_delete)