from classes import Functions
from art import text2art as font
def main():
    colors =Functions.UserUtilities.colors()
    wolcome=font("PrimeLibrary", font='small')
    print(f"{colors['Blue']} {wolcome}")
    print("-"*15 , "Wolcome", "-"*15)
    utilities = Functions.UserUtilities()
    utilities.lists()
if __name__ == "__main__":
    main()