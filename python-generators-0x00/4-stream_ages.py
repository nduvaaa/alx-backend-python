#!/usr/bin/python3
import seed

def stream_user_ages():
    """Generator that yields user ages one at a time"""
    connection = seed.connect_to_prodev()
    cursor = connection.cursor()
    
    # Stream ages without loading all at once
    cursor.execute("SELECT age FROM user_data")
    while True:
        row = cursor.fetchone()
        if row is None:
            break
        yield row[0]
    
    cursor.close()
    connection.close()

def calculate_average_age():
    """Calculates average age using the generator"""
    total = 0
    count = 0
    
    # Single loop to process all ages
    for age in stream_user_ages():
        total += age
        count += 1
    
    if count == 0:
        return 0  # Avoid division by zero
    
    return total / count

if __name__ == "__main__":
    average = calculate_average_age()
    print(f"Average age of users: {average:.2f}")
