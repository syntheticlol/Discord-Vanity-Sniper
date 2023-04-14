import threading
import socket
import requests

id = input("Guild ID > ")
vanity = input("Vanity URL (example: bell, dog) > ")
token = input("Your Token > ")

def check_vanity():
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(3)
            s.connect(('discord.com', 443))
            headers = {
                'Authorization': token,
                'Content-Type': 'application/json'
            }
            response = requests.get(
                f'https://discord.com/api/v9/invites/{vanity}',
                headers=headers
            )
            if response.status_code == 404:
                print(f"Vanity {vanity} is available, claiming...")
                response = requests.patch(
                    f'https://discord.com/api/v9/guilds/{id}/vanity-url',
                    headers=headers,
                    json={'code': vanity}
                )
                if response.status_code == 200:
                    print("Vanity successfully claimed...")
                    return
                else:
                    print("Failed to claim vanity.")
            elif response.status_code == 200:
                print(f"Vanity {vanity} is taken.")
            else:
                print(f"Error checking vanity {vanity}")
            s.close()
        except Exception as e:
            print(f"Error connecting to Discord")
            continue

threads = []
for i in range(10):
    t = threading.Thread(target=check_vanity)
    threads.append(t)
    t.start()

for t in threads:
    t.join()
