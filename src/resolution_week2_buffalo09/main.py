import argparse
import os
import sys
import json

CONTACTS_FILE = "contacts.json"
def load():
    if not os.path.exists(CONTACTS_FILE):
        return []
    with open(CONTACTS_FILE, "r") as file:
        return json.load(file)

def save_contacts(contacts):
    with open(CONTACTS_FILE, "w") as file:
        json.dump(contacts, file, indent = 2)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-a" ,"--add", help = "Add a contact")
    parser.add_argument("-l" , "--list", help = "List all contacts", action = "store_true")
    parser.add_argument("-d", "--delete", help = "delete a contact using ID", type = int)
    args = parser.parse_args()

    if args.add:
        name = args.add.strip()
        contacts = load()
        if len(contacts) == 0:
            id = 1
        else:
            id = 1 + contacts[-1]["id"]
        contacts.append({
            "name": name, 
            "id": id, 
        })
        save_contacts(contacts)
        print(f"Added contact {name}")
    elif args.list:
        contacts = load()
        if len(contacts) == 0:
            print("none found")
        else:
            for contact in contacts:
                print(f"Name: {contact['name']}")
    elif args.delete:
        contacts = load()
        for contact in contacts:
            if contact["id"] == args.delete:
                contacts.remove(contact)
                save_contacts(contacts)
                print(f"Contact {args.delete} removed")


if __name__ == "__main__":
    main()