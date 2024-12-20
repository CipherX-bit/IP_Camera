import shodan
import os
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# Replace with your Shodan API key
SHODAN_API_KEY = 'SHODAN_API_KEY'

# List of countries and their codes
COUNTRIES = [
    ("United States", "US"),
    ("France", "FR"),
    ("Germany", "DE"),
    ("United Kingdom", "GB"),
    ("Canada", "CA"),
    ("Australia", "AU"),
    ("India", "IN"),
    ("China", "CN"),
    ("Japan", "JP"),
    ("Russia", "RU"),
    ("Brazil", "BR"),
    ("South Africa", "ZA"),
]

def clear_screen():
    """Clear the terminal screen."""
    os.system("cls" if os.name == "nt" else "clear")

def display_logo():
    """Display the program logo."""
    clear_screen()
    logo = r"""
 dP  888888ba      a88888b.                                                
 88  88    `8b    d8'   `88                                                
 88 a88aaaa8P'    88        .d8888b. 88d8b.d8b. .d8888b. 88d888b. .d8888b. 
 88  88           88        88'  `88 88'`88'`88 88ooood8 88'  `88 88'  `88 
 88  88           Y8.   .88 88.  .88 88  88  88 88.  ... 88       88.  .88 
 dP  dP            Y88888P' `88888P8 dP  dP  dP `88888P' dP       `88888P8                                                                                                                                             
"""
    print(Fore.GREEN + logo)
    print(Fore.RED + "   By CipherX (https://github.com/YassineDouadi)\n")

def display_country_list():
    """Display the list of countries."""
    clear_screen()
    print(Fore.CYAN + "\nList of Countries:")
    for index, (country, _) in enumerate(COUNTRIES, start=1):
        print(Fore.YELLOW + f"[{index}] {country}")
    print(Fore.YELLOW + "[0] Go Back to Main Menu")

def get_ip_cameras_by_country():
    """Fetch IP cameras for a selected country."""
    api = shodan.Shodan(SHODAN_API_KEY)
    try:
        credits = api.info()['query_credits']
        if credits <= 0:
            print(Fore.RED + "Insufficient query credits. Please upgrade your API plan or wait for credits to reset.")
            return
    except shodan.APIError as e:
        print(Fore.RED + f"Error checking API credits: {e}")
        return

    while True:
        display_country_list()
        try:
            choice = int(input(Fore.CYAN + "\nSelect a country by number (0 to go back): ").strip())
            if choice == 0:
                return  # Go back to the main menu
            if 1 <= choice <= len(COUNTRIES):
                country_name, country_code = COUNTRIES[choice - 1]
                print(Fore.GREEN + f"\nFetching IP cameras for {country_name} ({country_code})...\n")

                # Define the query for IP cameras
                query = f'webcam country:{country_code}'

                try:
                    results = api.search(query)

                    print(Fore.GREEN + f"Total results found: {results['total']}\n")

                    # Print the results
                    for result in results['matches']:
                        ip = result['ip_str']
                        port = result.get('port', 'N/A')
                        location = result.get('location', {})
                        city = location.get('city', 'Unknown')
                        print(Fore.YELLOW + f"IP: {ip}, Port: {port}, City: {city}\n")
                except shodan.APIError as e:
                    print(Fore.RED + f"Error: {e}")
                return
            else:
                print(Fore.RED + "Invalid choice. Please select a valid number.")
        except ValueError:
            print(Fore.RED + "Invalid input. Please enter a number.")

def about_us():
    """Display information about the program."""
    print(Fore.WHITE + """
    About Us:
    This program allows users to query IP cameras using the Shodan API.
    It is designed for educational and research purposes only. Please use responsibly.
    """)

def help_menu():
    """Display the help menu."""
    print(Fore.WHITE + """
    Help:
    [1] IP Address Camera: Search for IP cameras based on country.
    [2] About Us: Learn about the program.
    [3] Help: Display this help menu.
    [4] Update IP Camera: Feature not implemented in this version.
    [x] Exit: Close the program.
    """)

def update_ip_camera():
    """Placeholder for future update feature."""
    print(Fore.CYAN + "Update IP Camera: This feature is under construction. Stay tuned!")

def main():
    """Main function."""
    api = shodan.Shodan(SHODAN_API_KEY)
    try:
        info = api.info()
        print(Fore.GREEN + "API Key is valid. Usage stats:")
        print(info)
    except shodan.APIError as e:
        print(Fore.RED + f"Error: {e}")
        return

    display_logo()
    while True:
        print(Fore.CYAN + """
        Main Menu:
        [1] IP Address Camera.
        [2] About Us.
        [3] Help.
        [4] Update IP Camera.
        [x] Exit.
        """)
        choice = input(Fore.CYAN + " Enter your choice: ").strip().lower()

        if choice == '1':
            clear_screen()
            get_ip_cameras_by_country()
        elif choice == '2':
            clear_screen()
            about_us()
        elif choice == '3':
            clear_screen()
            help_menu()
        elif choice == '4':
            clear_screen()
            update_ip_camera()
        elif choice == 'x':
            clear_screen()
            print(Fore.GREEN + "Exiting the program. Goodbye!")
            break
        else:
            print(Fore.RED + "Invalid choice. Please try again.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(Fore.RED + "\nProgram interrupted. Exiting.")
