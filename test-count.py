def print_divisible_by_3_or_5_not_15(file_path):

    
        with open(file_path, 'r') as file:
            for line in file:
             
                num = int(line.strip())
                
        
                if (num % 3 == 0 or num % 5 == 0) and num % 15 != 0:
                    print(num)
                    

file_path = 'numbers' 
print_divisible_by_3_or_5_not_15(file_path)
