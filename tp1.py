# la classe fait peut se comporter comme un fait ou comme une conclusion puisque les deux ont seulement les attribut valeur et atrribut
class Fait:
    def __init__(self, att='', val='', unsplitted=''):
        self.attribut = att
        self.valeur = val
        self.unsplitted = unsplitted

    # checks if fait mawjoud fel base des faits
    def exists(self, base_faits):
        for fait in base_faits:
            if (self.attribut.upper() == fait.attribut.upper()):
                return True
        return False


class Regle:

    def __init__(self, prem=[], conc=None, unsplitted=''):
        self.premises = prem
        self.conclusion = conc
        self.desactive = 0
        self.unsplitted = unsplitted

    def verif(self, faits):
        for premise in self.premises:
            if (premise.verif(faits) == False):
                return False
        return True

    # trace houa l fichier log contenant l'ajout des faits fel base des faits
    # executed houa tableau de taille = taille de tableau des regles w il est initialisé a faux lkol
    # i est l'indice du tableau de régles (et regles_executed)
    def execute(self, trace, regles_executed, base_faits, i):
        regles_executed[i] = True
        if (self.conclusion.exists(base_faits) == False):
            base_faits.append(self.conclusion)

        trace += "\n Ajout du fait:   " + self.conclusion.attribut + " = " + self.conclusion.valeur
        return None

    # retourne la conclusion de la regle
    def concl(self):
        self.desactive = 1
        return self.conclusion


class Premisse:
    def __init__(self, att='', val='', oper='='):
        self.attribut = att
        self.valeur = val
        self.operande = oper

    def verif(self, faits):
        for fait in faits:
            if (self.operande == "=" or self.operande == "=="):
                if (fait.attribut.upper() == self.attribut.upper() and fait.valeur.upper() == self.valeur.upper()):
                    return True
            if (self.operande == ">"):
                if (fait.attribut.upper() == self.attribut.upper() and int(fait.valeur) > int(self.valeur.upper())):
                    return True
            if (self.operande == ">="):
                if (fait.attribut.upper() == self.attribut.upper() and int(fait.valeur) >= int(self.valeur.upper())):
                    return True
            if (self.operande == "<="):
                if (fait.attribut.upper() == self.attribut.upper() and int(fait.valeur) <= int(self.valeur.upper())):
                    return True
            if (self.operande == "<"):
                if (fait.attribut.upper() == self.attribut.upper() and int(fait.valeur) < int(self.valeur.upper())):
                    return True
            if (self.operande == "!="):
                if (fait.attribut.upper() == self.attribut.upper() and fait.valeur.upper() != self.valeur.upper()):
                    return True

        return False


# fonction pour initialiser le tableau executed
def create_executed_tab(regles):
    tab = []
    for regle in regles:
        tab.append(False)
    return tab


# le type est par defaut chainage en avant "ch_avant"
# option est par defaut saturation de la base "sat_base"
class Base:
    def __init__(self, reglesurl="villes/regles.txt", faitsurl="villes/bf.txt", type="ch_avant", option="sat_base", ):
        self.reglesURL = reglesurl
        self.faitURL = faitsurl
        self.type = type
        self.option = option
        self.baseFaits = []
        self.baseRegles = []
        self.reglesFiltres = []
        self.trace = ''
        self.butFound = 0

    def chargerbase(self):
        fileRegles = open(self.reglesURL, "r", encoding='utf-8')
        f1 = fileRegles.readlines()
        for line in f1:
            # chargement des regles
            lineTemp = line.strip().split("si ", 1)[-1]
            premisses = lineTemp.split("alors ", 1)[0].strip()
            conclusionLine = lineTemp.split("alors ", 1)[-1].strip()
            conclusion = Fait()
            conclusion.unsplitted = conclusionLine
            conclusion.attribut = conclusionLine.split("=", 1)[0].strip()
            conclusion.valeur = conclusionLine.split("=", 1)[-1].strip()

            if (len(premisses.split("& ")) > 1):
                premissesLine = premisses.split("& ")
            else:
                premissesLine = premisses.split("et ")

            premissesTab = []
            for prem in premissesLine:
                premisse = Premisse()
                if (len(prem.split("==")) > 1):
                    premisse.attribut = prem.split("==")[0].strip()
                    premisse.operande = "=="
                    premisse.valeur = prem.split("==")[-1].strip()
                elif (len(prem.split("!=")) > 1):
                    premisse.attribut = prem.split("!=")[0].strip()
                    premisse.operande = "!="
                    premisse.valeur = prem.split("!=")[-1].strip()
                elif (len(prem.split(">=")) > 1):
                    premisse.attribut = prem.split(">=")[0].strip()
                    premisse.operande = ">="
                    premisse.valeur = prem.split("=")[-1].strip()
                elif (len(prem.split("<=")) > 1):
                    premisse.attribut = prem.split("<=")[0].strip()
                    premisse.operande = "<="
                    premisse.valeur = prem.split("<=")[-1].strip()
                elif (len(prem.split("=")) > 1):
                    premisse.attribut = prem.split("=")[0].strip()
                    premisse.operande = "="
                    premisse.valeur = prem.split("=")[-1].strip()
                elif (len(prem.split("<")) > 1):
                    premisse.attribut = prem.split("<")[0].strip()
                    premisse.operande = "<"
                    premisse.valeur = prem.split("<")[-1].strip()
                elif (len(prem.split(">")) > 1):
                    premisse.attribut = prem.split(">")[0].strip()
                    premisse.operande = ">"
                    premisse.valeur = prem.split(">")[-1].strip()

                premissesTab.append(premisse)

            self.baseRegles.append(Regle(premissesTab, conclusion, line))
        # chargement des faits
        fileFaits = open(self.faitURL, "r", encoding='utf-8')
        f2 = fileFaits.readlines()
        for line in f2:
            fait = Fait()
            fait.unsplitted = line
            fait.attribut = line.strip().split("= ")[0].strip()
            fait.valeur = line.strip().split("= ")[-1].strip()
            self.baseFaits.append(fait)
        return None

    # retourne une liste avec les regles déclenchables,
    def filtrerRegles(self):
        self.trace += '*******  Filtrage des regles déclenchables *******: \n'
        self.reglesFiltres = []
        for regle in self.baseRegles:
            if regle.verif(self.baseFaits) and regle.desactive == 0:
                print('regle non desactive trouvee')
                self.reglesFiltres.append(regle)
                self.trace += regle.unsplitted + '\n'
        return self.reglesFiltres

    def choisirRegle(self):
        print('choisir regle')
        self.trace += '******* On choisit la regle ******** : \n' + self.reglesFiltres[0].unsplitted + '\n'
        return self.reglesFiltres[0]

    def union(self, conclusion: Fait):
        if conclusion.exists(self.baseFaits):
            print('conclusion existe déja dans BF')
            return
        else:
            print('conclusion nexiste pas dans BF, donc UNION')

            self.baseFaits.append(conclusion)
            self.trace += "******* Ajout du fait ******* : \n" + conclusion.attribut + " = " + conclusion.valeur + '\n'


# base.chargerbase()


# For Testing Chargement de la Base
# print("Faits \n")
# for fait in base.baseFaits:
#     print(fait.attribut)
#     print(fait.valeur)
# for regle in base.baseRegles:
#     print("#Conclusion \n")
#     print(regle.conclusion.valeur)
#     print(regle.conclusion.attribut)
#     print("#Premisses \n")
#     for premisse in regle.premises:
#         print(premisse.attribut)
#         print(premisse.operande)
#         print(premisse.valeur)

# algorithme de saturation
def saturerBF(base: Base):
    while len(base.filtrerRegles()) > 0:
        # choix de la regle et la desactivation
        regle = base.choisirRegle()

        # ajout de la regle dans la BF
        base.union(regle.concl())

    base.trace += 'FIN DE SATURATION DE LA BASE\n\n'
    base.trace += '******* Nouvelle Base des faits: ******* \n'
    for fait in base.baseFaits:
        base.trace += fait.unsplitted + '\n'
    print(base.trace)
    outF = open("result.txt", "w+", encoding='utf-8')
    outF.write(base.trace)
    outF.close()


# Le butString dans ce cas est une chaine dédiée à partir de l'Interface UI
# exemple le butString= "Très bons restaurants= Vrai
def chercherBut(butString, base: Base):
    print('chercher but')
    but = Fait()
    but.attribut = butString.strip().upper().split("=")[0].strip()
    but.valeur = butString.strip().upper().split("=")[-1].strip()
    if (but.exists(base.baseFaits) == True):
        base.trace += "\n Le But " + but.attribut + " = " + but.valeur + " a été trouvé"
        print(base.trace)
        outF = open("result.txt", "w+", encoding='utf-8')
        outF.write(base.trace)
        outF.close()
        return True
    while len(base.filtrerRegles()) > 0:
        # choix de la regle et la desactivation
        regle = base.choisirRegle()

        # ajout de la regle dans la BF
        base.union(regle.concl())
        if (but.exists(base.baseFaits)):
            base.trace += "\n Le But " + but.attribut + " = " + but.valeur + " a été trouvé"
            print(base.trace)
            base.butFound = 1
            outF = open("result.txt", "w+", encoding='utf-8')
            outF.write(base.trace)
            outF.close()
            return True
    base.trace += "\n Le But " + but.attribut + " = " + but.valeur + " n'a pas été trouvé"
    print(base.trace)
    outF = open("result.txt", "w+", encoding='utf-8')
    outF.write(base.trace)
    outF.close()
    return False

# saturerBF()

# chercherBut("TrÃ¨s bons restaurants = Vrai", Base())
