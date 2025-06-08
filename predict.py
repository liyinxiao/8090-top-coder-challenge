import sys
import joblib
import pandas as pd

def ends_with_49(x):
    return round(x % 1, 2) == 0.49

def ends_with_99(x):
    return round(x % 1, 2) == 0.99

def calculate_reimbursement(trip_duration_days, miles_traveled, total_receipts_amount):
    # Load the model from the file
    loaded_model = joblib.load('gbr_model_final.pkl')

    miles_traveled_per_day = miles_traveled / trip_duration_days * 1.0

    data = [{
        'trip_duration_days': trip_duration_days,
        'miles_traveled': miles_traveled,
        'total_receipts_amount': total_receipts_amount,
        'miles_traveled_per_day': miles_traveled_per_day,
        'total_receipts_amount_per_day': total_receipts_amount / trip_duration_days * 1.0,
        'day_5': 1 if trip_duration_days == 5 else 0,
        'day_6': 1 if trip_duration_days == 6 else 0,
        'day_7_or_8': 1 if trip_duration_days == 7 or trip_duration_days == 8 else 0,
        'ends_with_49_99': 1 if ends_with_49(total_receipts_amount) or ends_with_99(total_receipts_amount) else 0,
        'sweet_miles_traveled_per_day': 1 if miles_traveled_per_day > 180 and miles_traveled_per_day < 220 else 0,
    }]
    
    df = pd.DataFrame(data)

    score = round(float(loaded_model.predict(df)[0]), 2)
    
    return max(0, score)


if __name__ == "__main__":
    trip_duration_days = int(sys.argv[1])
    miles_traveled = float(sys.argv[2])
    total_receipts_amount = float(sys.argv[3])

    result = calculate_reimbursement(trip_duration_days, miles_traveled, total_receipts_amount)
    print(result)