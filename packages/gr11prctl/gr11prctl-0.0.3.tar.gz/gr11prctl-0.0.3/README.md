# **gr11prctl** 📚  
*A Python package with essential Grade 11 practical programs!*  

[![PyPI Version](https://img.shields.io/pypi/v/gr11prctl?color=blue)](https://pypi.org/project/gr11prctl/)  
[![License](https://img.shields.io/github/license/TanujairamV/gr11prctl)](https://github.com/TanujairamV/gr11prctl/blob/main/LICENSE)  
[![GitHub Repo](https://img.shields.io/badge/GitHub-Repo-blue?logo=github)](https://github.com/TanujairamV/gr11prctl)  

---

## 📌 **About**
`gr11prctl` is a Python package that provides a collection of **Grade 11 practical programs** to help students understand fundamental programming concepts through ready-to-use functions.

---

## 🚀 **Installation**
Install `gr11prctl` from PyPI using:  
```sh
pip install gr11prctl
```

---

## 🛠 **Usage**
### **1️⃣ View Available Programs**
To list all available programs, run:  
```python
import gr11prctl
gr11prctl.code()
```

### **2️⃣ Import and Use Specific Functions**
You can directly import functions from the `snippets` module.  
Example: **Check if a number is prime**
```python
from gr11prctl.snippets import is_prime
print(is_prime(7))  # Output: True
```

---

## 📜 **Available Programs**
| #  | Function Name | Description |
|----|-------------|-------------|
| 1  | `pattern1_code` | Prints a **right-angled triangle pattern**. |
| 2  | `perfect_number_code` | Checks if a number is **Perfect**. |
| 3  | `prime_number_code` | Determines if a number is **Prime or Composite**. |
| 4  | `fibonacci_series_code` | Generates the **Fibonacci sequence**. |
| 5  | `count_chars_code` | Counts **vowels, consonants, uppercase, and lowercase letters** in a string. |
| 6  | `palindrome_string_code` | Checks if a string is a **Palindrome**. |
| 7  | `swap_even_odd_code` | Swaps **even and odd-indexed elements** in a list. |
| 8  | `frequency_list_code` | Finds the **frequency of elements** in a list. |
| 9  | `search_tuple_code` | Searches for an item in a **tuple**. |
| 10 | `student_details_code` | Stores student details and **filters students with marks > 75**. |

---

## 🎯 **Example Usages**
### **🔹 Right-Angled Triangle Pattern**
```python
from gr11prctl.snippets import pattern1_code
exec(pattern1_code.code)
```
#### 🖥 Output (Example for `n=5`):
```
*  
* *  
* * *  
* * * *  
* * * * *  
```

---

### **🔹 Check if a Number is Prime**
```python
from gr11prctl.snippets import prime_number_code
exec(prime_number_code.code)
```
#### 🖥 Output:
```
Enter any number: 7
7 is a PRIME number
```

---

### **🔹 Fibonacci Series**
```python
from gr11prctl.snippets import fibonacci_series_code
exec(fibonacci_series_code.code)
```
#### 🖥 Output:
```
How many terms? 5
Fibonacci sequence:
0 , 1 , 1 , 2 , 3 ,
```

---

### **🔹 Swap Even and Odd Elements in a List**
```python
from gr11prctl.snippets import swap_even_odd_code
exec(swap_even_odd_code.code)
```
#### 🖥 Output:
```
Enter number of elements: 4
Enter element: 1
Enter element: 2
Enter element: 3
Enter element: 4
Original List: [1, 2, 3, 4]
List after swapping: [2, 1, 4, 3]
```
