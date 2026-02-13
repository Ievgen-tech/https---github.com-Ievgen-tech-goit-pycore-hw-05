import sys
from typing import List, Dict


def parse_log_line(line: str) -> Dict:
    """
    Parses a single log line and extracts its components.

    Expected log format: YYYY-MM-DD HH:MM:SS LEVEL Message...

    Args:
        line (str): A single line from the log file

    Returns:
        dict: Dictionary containing 'date', 'time', 'level', and 'message' keys.
              Returns empty dict if parsing fails.

    Example:
        >>> parse_log_line("2024-02-13 10:15:23 INFO User logged in")
        {'date': '2024-02-13', 'time': '10:15:23', 'level': 'INFO',
         'message': 'User logged in'}
    """
    try:
        # Strip whitespace from both ends
        line = line.strip()

        # Split the line into parts
        parts = line.split(maxsplit=3)

        # Check if we have minimum required parts: date, time, level, message
        if len(parts) < 4:
            return {}

        # Extract components
        return {
            'date': parts[0],
            'time': parts[1],
            'level': parts[2],
            'message': parts[3]
        }
    except (ValueError, IndexError):
        return {}


def load_logs(file_path: str) -> List[Dict]:
    """
    Loads and parses all logs from a file.

    Opens the file and applies parse_log_line to each line,
    storing results in a list.

    Args:
        file_path (str): Path to the log file

    Returns:
        list: List of parsed log entries (dictionaries)

    Raises:
        FileNotFoundError: If the log file does not exist
        IOError: If there's an error reading the file
    """
    logs = []

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                parsed = parse_log_line(line)
                # Only add successfully parsed logs
                if parsed:
                    logs.append(parsed)

        return logs

    except FileNotFoundError:
        print(f"Error: Log file '{file_path}' not found.", file=sys.stderr)
        sys.exit(1)
    except IOError as e:
        print(f"Error reading file '{file_path}': {e}", file=sys.stderr)
        sys.exit(1)


def count_logs_by_level(logs: List[Dict]) -> Dict[str, int]:
    """
    Counts the number of log entries for each logging level.

    Uses functional programming approach with lambda and dictionary comprehension.

    Args:
        logs (list): List of parsed log entries

    Returns:
        dict: Dictionary with log levels as keys and counts as values.
              Includes all standard levels: INFO, DEBUG, ERROR, WARNING

    Example:
        >>> logs = [{'level': 'INFO'}, {'level': 'ERROR'}, {'level': 'INFO'}]
        >>> count_logs_by_level(logs)
        {'INFO': 2, 'ERROR': 1, 'DEBUG': 0, 'WARNING': 0}
    """
    # Define all standard log levels
    standard_levels = ['INFO', 'DEBUG', 'ERROR', 'WARNING']

    # Use dictionary comprehension with filter() and lambda
    # This combines functional programming elements
    def count_by_level(level_name):
        return len(list(filter(lambda log: log.get('level') == level_name, logs)))

    level_counts = {level: count_by_level(level) for level in standard_levels}

    return level_counts


def filter_logs_by_level(logs: List[Dict], level: str) -> List[Dict]:
    """
    Filters log entries by a specific logging level.

    Uses built-in filter() function for functional programming approach.

    Args:
        logs (list): List of parsed log entries
        level (str): The logging level to filter by (e.g., 'ERROR', 'INFO')

    Returns:
        list: List of log entries matching the specified level

    Example:
        >>> logs = [{'level': 'INFO', 'message': 'test1'},
        ...         {'level': 'ERROR', 'message': 'test2'}]
        >>> filter_logs_by_level(logs, 'ERROR')
        [{'level': 'ERROR', 'message': 'test2'}]
    """
    # Use filter() with lambda for functional programming approach
    return list(filter(lambda log: log.get('level') == level.upper(), logs))


def display_log_counts(counts: Dict[str, int]):
    """
    Formats and displays log statistics in a table format.

    Displays the count of log entries for each logging level.

    Args:
        counts (dict): Dictionary with log levels and their counts

    Example:
        >>> counts = {'INFO': 4, 'DEBUG': 3, 'ERROR': 2, 'WARNING': 1}
        >>> display_log_counts(counts)
        Logging Level | Count
        --------------|-------
        INFO          | 4
        DEBUG         | 3
        ERROR         | 2
        WARNING       | 1
    """
    print("\n" + "="*30)
    print("Logging Level | Count")
    print("-" * 30)

    # Sort levels by count (descending) for better readability
    sorted_counts = sorted(counts.items(), key=lambda item: item[1], reverse=True)

    for level, count in sorted_counts:
        # Format output with proper alignment
        print(f"{level:<13} | {count}")

    print("="*30 + "\n")


def main():
    """
    Main function that orchestrates the log analysis workflow.

    Handles command-line arguments:
    - First argument: path to log file (required)
    - Second argument: log level to filter by (optional)
    """
    # Check command-line arguments
    if len(sys.argv) < 2:
        print("Usage: python cabin.py <log_file> [<log_level>]", file=sys.stderr)
        print("Example: python cabin.py logs.log", file=sys.stderr)
        print("Example: python cabin.py logs.log ERROR", file=sys.stderr)
        sys.exit(1)

    log_file = sys.argv[1]
    filter_level = sys.argv[2].upper() if len(sys.argv) > 2 else None

    # Load logs from file
    print(f"Loading logs from '{log_file}'...")
    logs = load_logs(log_file)

    if not logs:
        print("No valid log entries found in the file.", file=sys.stderr)
        sys.exit(1)

    print(f"Successfully loaded {len(logs)} log entries.\n")

    # Count logs by level
    counts = count_logs_by_level(logs)

    # Display statistics
    display_log_counts(counts)

    # If a specific level was requested, filter and display
    if filter_level:
        filtered_logs = filter_logs_by_level(logs, filter_level)

        if not filtered_logs:
            print(f"No log entries found with level '{filter_level}'.\n")
        else:
            print(f"\nDetails for '{filter_level}' level ({len(filtered_logs)} entries):")
            print("-" * 80)

            # Display filtered logs with formatting
            for log in filtered_logs:
                timestamp = f"{log['date']} {log['time']}"
                message = log['message']
                print(f"[{timestamp}] {message}")

            print("-" * 80 + "\n")


if __name__ == "__main__":
    main()
