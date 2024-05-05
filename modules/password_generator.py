import random
from colorama import Fore, init

def password_gen():
  import string
  init(autoreset=True)
  numbers = list(range(1, 10))
  uppercase_letters = list(string.ascii_uppercase)
  lowercase_letters = list(string.ascii_lowercase)
  special_characters = ['!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/', ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`', '{', '|', '}', '~']
  combined_list = numbers + uppercase_letters + lowercase_letters + special_characters
  new = []
  q = input("password length: ")
  for i in range(int(q)):
    new.append(str(random.choice(combined_list)))
  password =  str(''.join(new))
  
  print("\nPassword of " + Fore.YELLOW + str(q) + Fore.WHITE + " characters is " + Fore.YELLOW + password + "\n")








