class CodeSnippet:
    def __init__(self, code):
        self.code = code

# 1. Display Right-Angled Triangle Pattern (*)
pattern1_code = CodeSnippet("""\
rows = int(input("Enter the number of rows: "))
for i in range(1, rows + 1):
    print("* " * i)
""")

# 2. Determine Perfect Number
perfect_number_code = CodeSnippet("""\
number = int(input("Enter the number: "))
sum1 = 0
for i in range(1, number):
    if number % i == 0:
        sum1 += i
if sum1 == number:
    print(number, "is a Perfect number")
else:
    print(number, "is not a Perfect number")
""")

# 3. Prime/Composite Number
prime_number_code = CodeSnippet("""\
num = int(input("Enter any number: "))
if num > 1:
    for i in range(2, num):
        if (num % i) == 0:
            print(num, "is NOT a PRIME number, it is a COMPOSITE number")
            break
    else:
        print(num, "is a PRIME number")
elif num == 0 or num == 1:
    print(num, "is neither Prime NOR Composite number")
""")

# 4. Fibonacci Series
fibonacci_series_code = CodeSnippet("""\
nterms = int(input("How many terms? "))
n1, n2 = 0, 1
count = 0
if nterms <= 0:
    print("Please enter a positive integer")
elif nterms == 1:
    print("Fibonacci sequence up to", nterms, ":", n1)
else:
    print("Fibonacci sequence:")
    while count < nterms:
        print(n1, end=" , ")
        nth = n1 + n2
        n1 = n2
        n2 = nth
        count += 1
""")

# 5. Count Vowels, Consonants, Uppercase, and Lowercase in a String
count_chars_code = CodeSnippet("""\
text = input("Enter a string: ")
vowels = "aeiouAEIOU"
vowel_count = 0
consonant_count = 0
uppercase_count = 0
lowercase_count = 0
                               
for char in text:
    if char.isalpha():
        if char in vowels:
            vowel_count += 1
        else:
            consonant_count += 1
        if char.isupper():
            uppercase_count += 1
        else:
            lowercase_count += 1

print("Number of Vowels:", vowel_count)
print("Number of Consonants:", consonant_count)
print("Number of Uppercase Letters:", uppercase_count)
print("Number of Lowercase Letters:", lowercase_count)
""")

# 6. Check if a String is a Palindrome
palindrome_string_code = CodeSnippet("""\
text = input("Enter a string: ")
if text == text[::-1]:
    print(text, "is a Palindrome")
else:
    print(text, "is NOT a Palindrome")
""")

# 7. Swap Elements in a List (Even and Odd Positions)
swap_even_odd_code = CodeSnippet("""\
l = []
n = int(input("Enter number of elements: "))
for i in range(n):
    l.append(int(input("Enter element: ")))
print("Original List:", l)
for i in range(0, len(l)-1, 2):
    l[i], l[i+1] = l[i+1], l[i]
print("List after swapping:", l)
                                 
""")

# 8. Frequency of Elements in a List
frequency_list_code = CodeSnippet("""\
l = [1,2,3,4,5,1,2,3,4,1,2,1]
ele = []
freq = []
for i in l:
    if i not in ele:
        ele.append(i)
        freq.append(l.count(i))
print("Element Frequency")
for i in range(len(ele)):
    print(ele[i], freq[i])                                
""")

# 9. Search an Item in a Tuple
search_tuple_code = CodeSnippet("""\
t = ()
n = int(input("Enter number of elements: "))
for i in range(n):
    t += (int(input("Enter element: ")))
print("Tuple:", t)
ele = int(input("Enter element to search: "))
if ele in t:
    print(ele, "found at index", t.index(ele))
else:
    print(ele, "not found in tuple")
""")

# 10. Store Student Details and Find Those with Marks > 75
student_details_code = CodeSnippet("""\
no_of_std = int(input("Enter number of students: "))
result = {}
for i in range(no_of_std):
    print("Enter Details of student No.", i+1)
    roll_no = int(input("Roll No: "))
    std_name = input("Student Name: ")
    marks = int(input("Marks: "))
    result[roll_no] = [std_name, marks]

print(result)
print("Students with marks > 75:")
for student in result:
    if result[student][1] > 75:
        print(result[student][0])
""")
