#Purpose of this program is to generate prime numbers in binary
#Also shows how as the number of binary digits increase, so does the amount of time to find a prime number

import random
import math
import time

def addition(x, y):
    #Input: Two integers x and y as vectors containing only 1, or 0s
    #Output: the sum of the two integers in binary
    
    #checking to see if the y vector has the same length as x
    if(len(x) > len(y)):
        difference = len(x) - len(y)
        for i in range(0, difference, 1):
            y.append(0)        
    elif(len(x) < len(y)):
        difference = len(y) - len(x)
        for i in range(0, difference, 1):
            x.append(0)        
    
    #initalizing the carry variable
    c = 0 
    result = []
    for i in range(0, len(x)):
        if((c + x[i] + y[i]) == 1 or (c + x[i] + y[i]) == 3):
            result.append(1)
        elif((c + x[i] + y[i]) == 2 or (c + x[i] + y[i]) == 0):
            result.append(0)   
        
        if((c + x[i] + y[i]) >= 2):
            c = 1
        else:
            c = 0
    if(c == 1):
        result.append(1)
    return result


def bin2Dec(n):
#Input: a binary number in an array
#Output: A decimal degit

    dec = 0
    for i in range(0, len(n), 1):
        if(n[i] == 1):
            dec = dec + (2 ** i)
    return dec

def bruteCheck(n):
    #Input: an integer n that could be a prime number
    #Output: True if it is a prime number and False if it isn't
    
    limit = math.sqrt(n) #taking the square root of the number to be checked
    i = 3 #initalizing the counter at 3 to see if the number being checked is prime or not.
    
    complete = False
    result = True #assuming that the number being checked is prime
    
    while(complete == False):
        if(i < limit):
            if((n % i) == 0): 
                complete = True 
                result = False #the number isn't being checked
            else:
                i += 1
        else:
            complete = True
    return result

def createNumber(n):
# Input: the amount of bits that the prime number is going to be
# A prime number
    random.seed()
    binaryNum = [1] # Each number will have to start with a 1
  
    for i in range(0, n):
        binaryNum.append(random.randrange(0, 2, 1))
    binaryNum.append(1)
    
    return binaryNum


def divide(x, y):
#Input: Two integers x and y, where x >= 0, y > 0
#Output: The remainder of x divided by y
    r = []
    for i in range(len(x) - 1, -1, -1):
        r = [0] + r
        if(x[i] == 1):
            r = addition(r[:], [1])
        if(greater(r[:], y[:])):
            r = subtract(r[:], y[:])
    return r

def greater(r, y):
    #Input: two integers in binary array form
    #Output: the greater between the two
    difference = 0
    
    #Padding the one with less digits
    if(len(r) < len(y)):
        difference = len(y) - len(r)
        for i in range(0, difference):
            r.append(0)
    elif(len(y) < len(r)):
        difference = len(r) - len(y)
        for i in range(0, difference):
            y.append(0)
    
    #Initializing variables for the while loop
    complete = False
    i = len(r) - 1
    result = r       
    
    while((complete == False) and (i >= 0)):
        if(i < len(r)):
            if(r[i] < y[i]):
                result = y
                complete = True
            elif(y[i] < r[i]):
                result = r
                complete = True
            else:
                i -= 1   
        else:
            complete = True
    if(result == r):    
        return True
    else:
        return False


def modexp(x, y, N):
#Input: a binary number y in an array and and integer N
#Output: The modular exponentiation of 3 ** y mod N

    z = [1]
    for i in range(len(y) - 1, -1, -1):
        z = divide(multiply(z[:], z[:]), N[:])
        if(y[i] == 1):
            z = divide(multiply(z[:], x[:]), N[:])
    
    return z


def multiply(x, y):
    #Input: Two n-bit integers x and y, where x, y >= 0
    #Output: Their product
    z = []
    for i in range(len(y) - 1, -1, -1):
        z = [0] + z
        if(y[i] == 1):
            z = addition(z[:], x[:])
           
    #remove the leading zeros.
    complete = False
    while(complete == False):
        if(z[-1] == 0 and len(z) > 1):
            z = z[:-1]
        else:
            complete = True
    return z


def primality(n):
#Input: an integer n
#Output: if the integer is 1, then the number is prime and will return true
    if(n == [1]):
        return True
    else:
        return False
    
def subtract(x, y):
    #Input: two integers in binary arrays with x >= y
    #Output: their difference
    
    #padding y with leading zeros so that size(y) = size(x)
    if(len(x) < len(y)):
        while(len(x) < len(y)):
            x.append(0)
    elif(len(y) < len(x)):
        while(len(y) < len(x)):
            y.append(0)
            
    difference = []       
    c = 0 
    
    for i in range(0, len(x), 1):
        if((c + x[i] + y[i]) % 2 == 1):
            difference.append(1)
        else:
            difference.append(0)
            
            
        if((c + y[i] + difference[i]) >= 2):
            c = 1
        else:
            c = 0
            
    complete = False
    while(complete == False):
        if(difference[-1] == 0 and len(difference) > 1):
            difference = difference[:-1]
        else:
            complete = True
        
    return difference
       
def main():    
    #How many binary numbers that will be produced
    amountOfBinaryNumbers = 100
    
    #How many bits that we want to the binary numbers to have
    numOfBits = 16
    
    #Taking away 2 from the input because the first and last digit has to be one and are
    bits2Generate = numOfBits - 2
    
    #Initalizing all arrays needed.
    primeNumbers = []  #number of prime numbers from binaryNum[]
    x = [1,1] #Will be the x in the modexp function
    
#------------ Creating 100 16-bit binary numbers ---------------------------------|

    while(len(primeNumbers) < 100):
        
        #Creating the binary number
        N = createNumber(bits2Generate)
        
        #subtractign one less from N for the modexp function.
        y = subtract(N[:], [1])
        
        result = modexp(x[:], y[:], N[:])
        
        #Checking to see if it is prime or not.
        if(primality(result)):
            
            #if prime then add it to the list of prime numbers.
            primeNumbers.append(N)
    
    #Initalizing the numbers that were not prime
    notPrime = 0
    
    #Checking by brute force if it is a real prime number or not.
    for i in primeNumbers:
        if(bruteCheck(bin2Dec(i)) == False):
            notPrime += 1
    print("By checking by brute force, I found that out of 100 binary 16-bit integers, ", notPrime, " were not prime.")
    print()
    
    #Start generating 16, 32, 64, 128 bit binary integers until a prime is found
    bitsToCreate = [16, 32, 64, 128] #Initalizing the list of bits that will need to be produced
    
    longPrime = [] #Initalizing the array for the 64 and 128 bit prime numbers



# |--------------- calculating how long it takes to create the first binary number ------------------------------------------|


    for i in range(0, len(bitsToCreate), 1):
        primeFound = False 
        primeTries = 1
        
        #Starting the clock to find the run time for the algorithm
        startTime = time.time()
        while(primeFound == False):
            
            bits2Generate = bitsToCreate[i] - 2 #The random binary number generator already had the first and last digit decided
        
            N = createNumber(bits2Generate)
            y = subtract(N[:], [1])
            result = modexp(x[:], y[:], N[:])
            #Checking to see if it is prime or not.
            if(primality(result)):
                primeFound = True #Prime was found!
                
                #Calculating the time it took to complete finding a prime number
                endTime = round(time.time() - startTime, 4)
                
                #reporting the run time
                print("Time to find a ", bitsToCreate[i], "bit prime number is: ", endTime, "and it took ", primeTries, "tries to find a prime.") #report run time
                print("It took on average ", round(endTime / primeTries, 4), "for the algorithm to complete.")
                print()
                
                #Holding onto the prime 64 and 128 bit numbers for reporting
                if(bitsToCreate[i] == 64 or bitsToCreate[i] == 128):
                    longPrime.append(N)
        
            else:
                primeTries += 1
                
    #printing out the 64 and 128-bit binary integers in binary and decimal form.
    print("The 64-bit integer was ", bin2Dec(longPrime[0]), " and here it is in binary:")
    print(longPrime[0])
    print()
    print("The 128-bit integer was ", bin2Dec(longPrime[1]), " and here it is in binary:")
    print(longPrime[1])
        
main()