class Pasek:
    def __init__(self, znak='#', start=0, szerokosc=20, pusto='-'):
        self.znak = znak
        self.start = start
        self.szerokosc = int(szerokosc)
        self.pusto = pusto

    def dalej(self, procent=0):
        linia = "{" + format(round(procent*100, 0), ".0f") + "%}["
        for i in range(self.szerokosc):
            wartosc = i + 1  # 0 + 1 = 1
            aktwartosc = wartosc / self.szerokosc  # 1 / 20 -> 0.05
            if aktwartosc <= procent:
                linia += self.znak
            else:
                linia += self.pusto
        linia += "]"
        print(linia, end="\r")

    def koniec(self):
        self.dalej(procent=1)