import requests
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed
import json

# Fetch user profile data (using a mock API endpoint)
def fetch_profile_data(username):
    try:
        # Mock API call: Replace with actual LeetCode API endpoint when available
        url = f"https://leetcode.com/api/profile/{username}"  # Hypothetical endpoint
        response = requests.get(url)
        
        if response.status_code != 200:
            raise Exception(f"Failed to fetch data for {username}. Status code: {response.status_code}")

        data = response.json()
        
        # Assume the response structure has 'rating', 'problems_solved', and 'badges'
        return {
            "Username": username,
            "Rating": data.get('rating', 'N/A'),
            "Problems Solved": data.get('problems_solved', 'N/A'),
            "Badges": ", ".join(data.get('badges', [])) if 'badges' in data else 'None'
        }
    except Exception as e:
        return {"Username": username, "Rating": "Error", "Problems Solved": "Error", "Badges": str(e)}

# Function to process a list of usernames
def fetch_profiles(usernames):
    profiles = []
    
    # Use ThreadPoolExecutor for concurrent requests
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(fetch_profile_data, username): username for username in usernames}
        for future in as_completed(futures):
            try:
                result = future.result()
                profiles.append(result)
            except Exception as e:
                profiles.append({"Username": futures[future], "Rating": "Error", "Problems Solved": "Error", "Badges": str(e)})
    
    return profiles

# Function to display data in a table format
def display_table(profiles):
    df = pd.DataFrame(profiles)
    print(df)

# Function to save data to CSV or JSON
def save_data(profiles, filename, filetype='csv'):
    df = pd.DataFrame(profiles)
    
    if filetype == 'csv':
        df.to_csv(filename, index=False)
    elif filetype == 'json':
        df.to_json(filename, orient='records', lines=True)

# Main function to accept input, fetch profiles, and display results
def main():
    # User input: either comma-separated list or file
    input_type = input("Enter input type (list/file): ").strip().lower()
    
    if input_type == 'list':
        usernames = input("Enter usernames (comma-separated): ").split(',')
    elif input_type == 'file':
        filename = input("Enter file name: ").strip()
        with open(filename, 'r') as file:
            usernames = [line.strip() for line in file.readlines()]
    else:
        print("Invalid input type. Please choose 'list' or 'file'.")
        return
    
    # Clean up usernames list (remove leading/trailing spaces)
    usernames = [username.strip() for username in usernames]
    
    # Fetch data for all usernames
    profiles = fetch_profiles(usernames)
    
    # Display the fetched profiles in a table format
    display_table(profiles)
    
    # Ask if user wants to save the results
    save_choice = input("Do you want to save the data? (y/n): ").strip().lower()
    if save_choice == 'y':
        save_format = input("Save as (csv/json): ").strip().lower()
        filename = input("Enter filename (e.g., profiles.csv): ").strip()
        save_data(profiles, filename, save_format)
        print(f"Data saved to {filename}")

if __name__ == '__main__':
    main()
