# Nessun import necessario

def main():
    conversione = input("Converti da (C)elsius a Fahrenheit o da (F)ahrenheit a Celsius? ")

    if conversione == "C":
        temperatura = float(input("Inserisci la temperatura in Celsius: "))
        temperatura_convertita = (temperatura * 9/5) + 32
        print(f"{temperatura:g}°C corrisponde a {temperatura_convertita:g}°F")
    elif conversione == "F":
        temperatura = float(input("Inserisci la temperatura in Fahrenheit: "))
        temperatura_convertita = (temperatura - 32) * 5/9
        print(f"{temperatura:g}°F corrisponde a {temperatura_convertita:g}°C")
    #else:
    #    print("Inserisci una convenzione corretta.")


if __name__ == "__main__":
    main()