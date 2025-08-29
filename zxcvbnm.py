import time, os, platform

# কালার কোড
rd, gn, lgn, yw, lrd, be, pe = '\033[00;31m', '\033[00;32m', '\033[01;32m', '\033[01;33m', '\033[01;31m', '\033[94m', '\033[01;35m'
cn, k, g = '\033[00;36m', '\033[90m', '\033[38;5;130m'

def re(text):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(0.001)

if 'Windows' in platform.uname():
    from colorama import init
    init()

banner = f"""
{k}        
        (                   
   (    )\\ )                
 ( )\\  (()/(      (    (    
 )((_)  /(_))     )\\   )\\   
((_)_  (_))    _ ((_) ((_)  
 | _ ) | |    | | | | | __| 
 | _ \\ | |__  | |_| | | _|  
 |___/ |____|  \\___/  |___| 
                             
"""

re(banner)
re("Warning ! This is a test reporter, any offense is the responsibility of the user !\n")
print(f"{lrd}")

# রঙের সাথে ক্রমিক লাইন আউটপুট
print(f"{lgn}1{lrd}  {gn}Reporter Channel{lrd}")
print(f"{lgn}2{lrd}  {gn}Reporter Account{lrd}")
print(f"{lgn}3{lrd}  {gn}Reporter Group [Updating]{lrd}")

number = input(f"{gn}Enter Number : {cn}")
if number == "1":
    os.system("python report/reporter.py")
elif number == "2":
    os.system("python report/report.py")
elif number == "3":
    print(f"{yw}This section is being updated and will be added soon\nChannel : @esfelurm{lrd}")