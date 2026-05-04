'''
Generator:
Function that behaves like an iterator (it can be used in a for loop)
Uses 'yield' instead of 'return'
Iterate without loading everything into memory (ex. reading laarge files)
return - Pouring Bucket
yield - drip faucet 
'''

def count_to(n):
    
    count = 1
    while count <=n:
        yield count
        count += 1
    


number = int(input("Enter a number to count to: "))

for n in count_to(number):
    print(n)


def read_file(file_path):
     with open(file_path) as file:
        for line in file:
            yield line.strip()
            

for line in read_file("/Users/adityabanerjee/Desktop/Nexflow-Marsh/Practice/text.txt"):
    print(line)