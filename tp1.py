class Regle:
    premises = []
    conclusion = []

    def __init__(self):
        self.premises = []
        self.conclusion = []


f = open("maladies/regles.txt", "r")
conclusion = []
premises = []
Regles = []
f1 = f.readlines()

for line in f1:
    print('--', line)
    x = line.split('alors', 1)[0].split('et')
    x[0] = x[0].split('si', 1)[1]

    R = Regle()
    for premise in x:
        print(premise)
        R.premises.append(premise)

        # exemple de recherche
        # if (premise.find('Douleur = "Gorge"')>0):
        #   print('trouve XXXXXXXXXXXXXXXX')

    print('------->>>>')

    y = line.split('alors', 1)[1].split('\n', 1)[0]
    print(y)
    # conclusion.append(y)
    R.conclusion.append(y)

    print('**************************')

    Regles.append(R)

#test1









