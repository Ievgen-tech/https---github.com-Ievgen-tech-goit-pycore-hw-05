from __future__ import annotations

from typing import Callable, Dict, List, Tuple


def input_error(func: Callable) -> Callable:
    """Handle user input errors and return friendly messages."""

    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Give me name and phone please."
        except KeyError:
            return "Enter user name."
        except IndexError:
            return "Enter the argument for the command."

    return inner


def parse_input(user_input: str) -> Tuple[str, List[str]]:
    """Parse user input into command and argument list."""
    user_input = user_input.strip()
    if not user_input:
        return "", []

    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, args


@input_error
def add_contact(args: List[str], contacts: Dict[str, str]) -> str:
    """Add a new contact to the address book."""
    if len(args) != 2:
        raise ValueError

    name, phone = args
    contacts[name] = phone
    return "Contact added."


@input_error
def change_contact(args: List[str], contacts: Dict[str, str]) -> str:
    """Update an existing contact phone number."""
    if len(args) != 2:
        raise ValueError

    name, phone = args
    if name not in contacts:
        raise KeyError

    contacts[name] = phone
    return "Contact updated."


@input_error
def show_phone(args: List[str], contacts: Dict[str, str]) -> str:
    """Return a phone number for a given contact name."""
    if len(args) != 1:
        raise ValueError

    name = args[0]
    if name not in contacts:
        raise KeyError

    return contacts[name]


@input_error
def show_all(contacts: Dict[str, str]) -> str:
    """Return all saved contacts in a readable format."""
    if not contacts:
        return "No contacts saved."

    lines = []
    for name, phone in contacts.items():
        lines.append(f"{name}: {phone}")
    return "\n".join(lines)


def main() -> None:
    """Run the interactive assistant bot loop."""
    contacts: Dict[str, str] = {}
    print("Welcome to the assistant bot!")

    while True:
        user_input = input("Enter a command: ")
        command, args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break
        if command == "hello":
            print("How can I help you?")
            continue
        if command == "add":
            print(add_contact(args, contacts))
            continue
        if command == "change":
            print(change_contact(args, contacts))
            continue
        if command == "phone":
            print(show_phone(args, contacts))
            continue
        if command == "all":
            print(show_all(contacts))
            continue

        if command == "":
            print("Enter a command.")
            continue

        print("Invalid command.")


if __name__ == "__main__":
    main()