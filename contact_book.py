"""Contact Book - a simple console application.

Features: add, view, search, update, delete contacts.
Data is saved in contacts.json so it persists between runs.
"""

import json
import os

FILE_NAME = "contacts.json"


def load_contacts():
    """Read contacts from the JSON file (returns an empty list if none)."""
    if not os.path.exists(FILE_NAME):
        return []
    try:
        with open(FILE_NAME, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []


def save_contacts(contacts):
    """Write contacts to the JSON file."""
    with open(FILE_NAME, "w") as f:
        json.dump(contacts, f, indent=4)


def show_contact(c, index=None):
    prefix = f"{index}. " if index is not None else ""
    print(f"{prefix}{c['name']} | Phone: {c['phone']} | "
          f"Email: {c['email']} | Address: {c['address']}")


def add_contact(contacts):
    name = input("Name: ").strip()
    if not name:
        print("Name cannot be empty.")
        return
    phone = input("Phone: ").strip()
    if not phone.isdigit() or len(phone) < 7:
        print("Please enter a valid phone number (digits only).")
        return
    if any(c["phone"] == phone for c in contacts):
        print("A contact with this phone number already exists.")
        return
    email = input("Email: ").strip()
    address = input("Address: ").strip()
    contacts.append({"name": name, "phone": phone,
                     "email": email, "address": address})
    save_contacts(contacts)
    print("Contact added successfully!")


def view_contacts(contacts):
    if not contacts:
        print("No contacts found.")
        return
    print("\n--- All Contacts ---")
    for i, c in enumerate(sorted(contacts, key=lambda x: x["name"].lower()), 1):
        show_contact(c, i)


def search_contacts(contacts):
    term = input("Search by name or phone: ").strip().lower()
    results = [c for c in contacts
               if term in c["name"].lower() or term in c["phone"]]
    if not results:
        print("No matching contacts.")
        return
    print(f"\nFound {len(results)} contact(s):")
    for i, c in enumerate(results, 1):
        show_contact(c, i)


def find_by_name(contacts, name):
    return [c for c in contacts if c["name"].lower() == name.lower()]


def update_contact(contacts):
    name = input("Enter the exact name of the contact to update: ").strip()
    matches = find_by_name(contacts, name)
    if not matches:
        print("Contact not found.")
        return
    contact = matches[0]
    print("Leave a field blank to keep the current value.")
    for field in ("name", "phone", "email", "address"):
        new_value = input(f"New {field} [{contact[field]}]: ").strip()
        if new_value:
            contact[field] = new_value
    save_contacts(contacts)
    print("Contact updated successfully!")


def delete_contact(contacts):
    name = input("Enter the exact name of the contact to delete: ").strip()
    matches = find_by_name(contacts, name)
    if not matches:
        print("Contact not found.")
        return
    confirm = input(f"Delete '{matches[0]['name']}'? (y/n): ").lower()
    if confirm == "y":
        contacts.remove(matches[0])
        save_contacts(contacts)
        print("Contact deleted.")
    else:
        print("Deletion cancelled.")


def main():
    contacts = load_contacts()
    actions = {
        "1": add_contact,
        "2": view_contacts,
        "3": search_contacts,
        "4": update_contact,
        "5": delete_contact,
    }
    while True:
        print("\n===== CONTACT BOOK =====")
        print("1. Add Contact")
        print("2. View All Contacts")
        print("3. Search Contact")
        print("4. Update Contact")
        print("5. Delete Contact")
        print("6. Exit")
        choice = input("Choose an option (1-6): ").strip()
        if choice == "6":
            print("Goodbye!")
            break
        action = actions.get(choice)
        if action:
            action(contacts)
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()