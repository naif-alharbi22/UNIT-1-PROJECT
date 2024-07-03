from classes import Functions , functions_admin
from art import text2art as font
def main():
    colors =Functions.UserUtilities.colors()
    wolcome=font("PrimeLibrary", font='small')
    print(f"{colors['Blue']} {wolcome}")
    print("-"*15 , "Wolcome", "-"*15)
    manager = functions_admin.Manager()
    manager.login_admin()
if __name__ == "__main__":
    main()