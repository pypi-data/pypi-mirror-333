# sources: 
# https://www.geeksforgeeks.org/generating-strong-password-using-python
# https://www.geeksforgeeks.org/create-a-random-password-generator-using-python/
#
# greatly improved by simon-seyock. Thx :)

import random
import array

def generate_password(user):
    """
    Generate a strong password for the db-users (login-roles).
    """ 

    # maximum length of password needed
    # this can be changed to suit your password length
    MAX_LEN = 30
    
    # declare arrays of the character that we need in out password
    # Represented as chars to enable easy string concatenation
    DIGITS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] 
    LOCASE_CHARACTERS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h',
                        'i', 'j', 'k', 'm', 'n', 'o', 'p', 'q',
                        'r', 's', 't', 'u', 'v', 'w', 'x', 'y',
                        'z']
    
    UPCASE_CHARACTERS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H',
                        'I', 'J', 'K', 'M', 'N', 'O', 'P', 'Q',
                        'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y',
                        'Z']
    
    SYMBOLS           = ['#', '$', '=', '?', '.', '|', '~', '>', 
                        '*', '(', ')', '<']
    
    # combines all the character arrays above to form one array
    COMBINED_LIST = DIGITS + UPCASE_CHARACTERS + LOCASE_CHARACTERS #+ SYMBOLS
    
    # randomly select at least one character from each character set above
    rand_digit = random.choice(DIGITS)
    rand_upper = random.choice(UPCASE_CHARACTERS)
    rand_lower = random.choice(LOCASE_CHARACTERS)
    rand_symbol = random.choice(SYMBOLS)
    
    # combine the character randomly selected above
    # at this stage, the password contains only 4 characters but
    # we want a 12-character password
    temp_pass = [rand_digit, rand_upper, rand_lower, rand_symbol]
    
    
    # now that we are sure we have at least one character from each
    # set of characters, we fill the rest of
    # the password length by selecting randomly from the combined
    # list of character above.
    for x in range(MAX_LEN - 4):
        temp_pass.append(random.choice(COMBINED_LIST))
    
    # convert temporary password into array and shuffle to
    # prevent it from having a consistent pattern
    # where the beginning of the password is predictable
    temp_pass_list = array.array('u', temp_pass)
    random.shuffle(temp_pass_list)
    
    # join chars to form password
    return "".join(temp_pass_list)