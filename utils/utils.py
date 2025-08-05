from datetime import datetime

PRIMARY_CLASSES = [f"Grade {i}" for i in range(1, 9)]

def format_date(db_date):
    """Convert '2024-05-30' to '30th May 2024'"""
    return datetime.strptime(db_date, "%Y-%m-%d").strftime("%d %B %Y")

def validate_borrow_date(date_str):
    """Prevent time-travel borrowing"""
    borrow_date = datetime.strptime(date_str, "%Y-%m-%d")
    if borrow_date > datetime.now():
        raise ValueError("Borrow date cannot be in the future!")

def get_student_class():
    """Dropdown for primary classes"""
    print("Select Class:")
    for i, cls in enumerate(PRIMARY_CLASSES, 1):
        print(f"{i}. {cls}")
    choice = int(input("Enter number: ")) - 1
    return PRIMARY_CLASSES[choice]