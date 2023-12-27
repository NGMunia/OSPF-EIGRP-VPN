from getpass import getpass
from rich import print as rp

username = input("Username: ")
password = getpass("password: ")
secret   = getpass("enable secret: ")

while True:
    if username == 'Automation' and password == 'cisco123' and secret == 'cisco123':
        rp('\n[bold green]LOGIN SUCCESSFUL![/bold green]\n')
        break  
    else:
        rp('[bold red]Incorrect Username and/or password!![/bold red]\n')
        username = input("Username: ")
        password = getpass("password: ")
        secret   = getpass("enable secret: ")