
# math_operations.py
# sample functions to generate Unit test code
def reverse_string(s):
    """Returns the reverse of the given string."""
    return s[::-1]

def capitalize_string(s):
    """Capitalizes the first letter of each word in the string."""
    return s.title()

def find_max_in_list(lst):
    """Returns the maximum element from a list."""
    if not lst:
        raise ValueError("List is empty.")
    return max(lst)

def calculate_average(lst):
    """Returns the average of a list of numbers."""
    if not lst:
        raise ValueError("List is empty.")
    return sum(lst) / len(lst)

def filter_even_numbers(lst):
    """Returns a list of even numbers from the given list."""
    return [num for num in lst if num % 2 == 0]

def get_user_role(user_dict, username):
    """Returns the role of a user from a dictionary of users."""
    return user_dict.get(username, "Guest")