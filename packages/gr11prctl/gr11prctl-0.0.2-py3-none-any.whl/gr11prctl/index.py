from gr11prctl.snippets import (
    pattern1_code,
    perfect_number_code,
    prime_number_code,
    fibonacci_series_code,
    count_chars_code,
    palindrome_string_code,
    swap_even_odd_code,
    frequency_list_code,
    search_tuple_code,
    student_details_code,
)

index_mapping = {
    "1": ("Display Right-Angled Triangle Pattern (*)", pattern1_code),
    "2": ("Determine Perfect Number", perfect_number_code),
    "3": ("Prime/Composite Number", prime_number_code),
    "4": ("Fibonacci Series", fibonacci_series_code),
    "5": ("Count Vowels, Consonants, Uppercase, and Lowercase in a String", count_chars_code),
    "6": ("Check if a String is a Palindrome", palindrome_string_code),
    "7": ("Swap Elements in a List (Even and Odd Positions)", swap_even_odd_code),
    "8": ("Frequency of Elements in a List", frequency_list_code),
    "9": ("Search an Item in a Tuple", search_tuple_code),
    "10": ("Store Student Details and Find Those with Marks > 75", student_details_code),
}

def code():
    print("\nSelect an experiment number:")
    for num, (desc, _) in index_mapping.items():
        print(f"{num}. {desc}")
    
    choice = input("\nEnter the experiment number: ")
    if choice in index_mapping:
        print("\n--- Source Code ---")
        print(index_mapping[choice][1].code)
    else:
        print("\nInvalid choice. Please select a valid experiment number.")

