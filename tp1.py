
#la classe fait peut se comporter comme un fait ou comme une conclusion puisque les deux ont seulement les attribut valeur et atrribut
class Fait:
    def __init__(self,att='',val=''):
        self.attribut = att
        self.valeur=val
    #checks if fait mawjoud fel base des faits
    def exists(self,base_faits):
        for fait in base_faits:
            if(self.attribut.upper()==fait.attribut.upper()):
                return True
        return False


class Regle:

    def __init__(self, prem=[],conc=None):
        self.premises = prem
        self.conclusion = conc

    def verif(self,faits):
        for premise in self.premises:
            if(premise.verif(faits)== False):
                return False
        return True


    #trace houa l fichier log contenant l'ajout des faits fel base des faits
    #executed houa tableau de taille = taille de tableau des regles w il est initialisé a faux lkol
    #i est l'indice du tableau de régles (et regles_executed)
    def execute(self,trace,regles_executed,base_faits,i):
        regles_executed[i]=True
        if(self.conclusion.exists(base_faits)==False):
            base_faits.append(self.conclusion)

        trace+= "\n Ajout du fait:   "+self.conclusion.attribut+" = "+self.conclusion.valeur
        return None


class Premisse:
    def __init__(self,att='',val='',oper='='):
        self.attribut=att
        self.valeur=val
        self.operande=oper

    def verif(self,faits):
         for fait in faits:
                if (self.operande == "=" or self.operande == "=="):
                    if (fait.attribut.upper() == self.attribut.upper() and fait.valeur.upper() == self.valeur.upper()):
                        return True
                if(self.operande== ">"):
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


#fonction pour initialiser le tableau executed
def create_executed_tab(regles):
    tab=[]
    for regle in regles:
        tab.append(False)
    return tab

#le type est par defaut chainage en avant "ch_avant"
#option est par defaut saturation de la base "sat_base"
class Base:
    def __init__(self,reglesurl="maladies/reg.txt",faitsurl="maladies/bf.txt",type="ch_avant",option="sat_base"):
        self.reglesURL=reglesurl
        self.faitURL=faitsurl
        self.type=type
        self.option=option
        self.baseFaits=[]
        self.baseRegles=[]

    def chargerbase(self):


        fileRegles=open(self.reglesURL,"r")
        f1 = fileRegles.readlines()
        for line in f1:
            # chargement des regles
            lineTemp=line.strip().split("si ",1)[-1]
            premisses=lineTemp.split("alors ",1)[0].strip()
            conclusionLine=lineTemp.split("alors ",1)[-1].strip()
            conclusion=Fait()
            conclusion.attribut=conclusionLine.split("=",1)[0].strip()
            conclusion.valeur=conclusionLine.split("=",1)[-1].strip()



            if(len(premisses.split("& "))>1):
                premissesLine=premisses.split("& ")
            else:
                premissesLine=premisses.split("et ")

            premissesTab=[]
            for prem in premissesLine:
                premisse=Premisse()
                if(len(prem.split("=="))>1):
                    premisse.attribut=prem.split("==")[0].strip()
                    premisse.operande="=="
                    premisse.valeur=prem.split("==")[-1].strip()
                elif (len(prem.split("!="))>1):
                    premisse.attribut = prem.split("!=")[0].strip()
                    premisse.operande = "!="
                    premisse.valeur = prem.split("!=")[-1].strip()
                elif (len(prem.split(">="))>1):
                    premisse.attribut = prem.split(">=")[0].strip()
                    premisse.operande = ">="
                    premisse.valeur = prem.split("=")[-1].strip()
                elif (len(prem.split("<="))>1):
                    premisse.attribut = prem.split("<=")[0].strip()
                    premisse.operande = "<="
                    premisse.valeur = prem.split("<=")[-1].strip()
                elif (len(prem.split("="))>1):
                    premisse.attribut = prem.split("=")[0].strip()
                    premisse.operande = "="
                    premisse.valeur = prem.split("=")[-1].strip()
                elif (len(prem.split("<"))>1):
                    premisse.attribut = prem.split("<")[0].strip()
                    premisse.operande = "<"
                    premisse.valeur = prem.split("<")[-1].strip()
                elif (len(prem.split(">"))>1):
                    premisse.attribut = prem.split(">")[0].strip()
                    premisse.operande = ">"
                    premisse.valeur = prem.split(">")[-1].strip()

                premissesTab.append(premisse)
            self.baseRegles.append(Regle(premissesTab,conclusion))
        #chargement des faits
        fileFaits = open(self.faitURL, "r")
        f2 = fileFaits.readlines()
        for line in f2:
            fait=Fait()
            fait.attribut=line.strip().split("= ")[0].strip()
            fait.valeur=line.strip().split("= ")[-1].strip()
            self.baseFaits.append(fait)
        return None


base=Base()
base.chargerbase()

#For Testing Chargement de la Base
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














