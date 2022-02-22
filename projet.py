import csv
# creation menu
def MENU():
    print("             MENU                 ")
    print("1: permet d'afficher les info")
    print("2:permet d'afficher une information par son numero")
    print("3:permet d'afficher les cinq premier")
    print("4: permet de modifier les donner invalide")
    print("0:pour quitter")

# verification numero


def validationnum(chaine):
    if len(chaine)!=7 or not chaine.isupper() or chaine.isalpha() or chaine.isdecimal() or  not chaine.isalnum() :
        return False
    else:
        return True
# verification prenom


def validation_PRENOM(chaine):
    chaine= chaine.strip()
    if len(chaine)<3 or not chaine[0].isalpha() or not chaine.isalnum():
        return False
    else:
        return True
# validation nom


def validation_NOM(chaine):
    chaine= chaine.strip()
    if len(chaine)<2 or not chaine[0].isalpha() or not chaine.isalnum():
        return False
    else:
        return True


def validation_CLASSE(chaine):
    chaine= chaine.strip()
    chaine= chaine.replace(" ","")
    if chaine =="":
        return False
    if chaine[0] in [range(3,7)] or chaine[-1] in ["A","B"]:
        return True
    else:
        return False


def date1(chaine):
    mois = {"ja": "1", "f": "2", "mars": "3", "av": "4", "mai": "5", "juin": "6", "juil": "7", "ao": "8", "sep": "9",
            "oct": "10", "nov": "11",
            "dec": "12"}
    chaine = chaine.strip()
    for x in chaine:
        if x in ["/", "-", ".", ",", ":", " ", "_", ".-", "-."]:
            chaine = chaine.split(x)
            break
    for keys in mois:
        if str(chaine[1].lower()).startswith(keys):
            chaine[1] = mois[keys]
            break
    liste = "/".join(chaine).replace(" ","/").replace("-","/").replace(".","/").replace(",","/")
    liste=liste.split("/")
    try:
        if (int(liste[-1])%4 == 0 and int(liste[-1])%100!= 0) or (int(liste[-1])%400== 0):
            if (int(liste[0]) < 1) or (int(liste[0]) > 31) or (int(liste[1]) < 1) or (int(liste[1]) > 12) or (
                        (int(liste[1]) == 2) and (int(liste[0]) > 29)):
                return False
            else:
                return True
        else:
            if (int(liste[0]) < 1) or (int(liste[0]) > 31) or (int(liste[0]) < 1) or (int(liste[1]) > 12) or (
                        (int(liste[1]) == 2) and (int(liste[1]) > 28)):
                return False
            else:
                return True
    except Exception as e:
        return False



document = open("papa.xlsx - Feuil2 (1).csv")
document1 = csv.DictReader(document)
tabT=[]
tabinv=[]
tabval=[]
for line in document1:
    line["Note"] = line["Note"].replace(",",";")
    if line["Numero"]==""or line["Nom"]=="" or line["Prénom"]==""or line["Date de naissance"]=="" or line["Classe"]=="" or line["Note"]=="" :
        tabinv.append(line)

    elif not validationnum(line["Numero"]) or not validation_PRENOM(line["Prénom"])or not validation_NOM(line["Nom"]) \
            or not validation_CLASSE(line["Classe"]) or not date1(line["Date de naissance"]):

        tabT.append(line)
    else:
        try:
            line["Note"] = line["Note"].split("#")
            d = {}
            for i in line["Note"]:
                i = i.split("[")
                i[1] = i[1].split("]")[0]
                d.setdefault(i[0], i[1])
                line["Note"] = d
            for i in line["Note"]:
                line["Note"][i] = line["Note"][i].split(":")
            liste1 = ["Devoir", "Exam"]
            moyin = 0
            for i in line["Note"]:
                line["Note"][i][0] = line["Note"][i][0].split(";")
                d = {k: v for k, v in zip(liste1, line["Note"][i])}
                d["Devoir"] = [float(c) for c in d["Devoir"]]
                d["Exam"] = float(d["Exam"])
                if (not d["Devoir"][0] or d["Devoir"][0] > 20) or (not d["Exam"] or d["Exam"] > 20):
                    tabinv.append(line)
                else:
                    moy = (((sum(d["Devoir"]) / len(d["Devoir"]) + 2 * d["Exam"]) / 3)).__round__(2)
                    d.setdefault("Moyenne", moy)
                    line["Note"][i] = d
                    moyin = moy + moyin
            moyG = (moyin / len(line["Note"])).__round__(2)
            line["Note"].setdefault("moyG", moyG)
            tabval.append(line)
        except Exception as e:
            tabinv.append(line)
Traiter=tabval
classement=[]
for i in range(len(Traiter)-1):
    listeclass=(Traiter[i]["Note"]["moyG"],i,Traiter[i]["Numero"])
    classement.append(listeclass)
classement.sort(reverse=True)

while True:
    MENU()
    try:
        a = int(input("donne un nombre entre 0 et 4:"))
        if a in range(0,5):
            if(a==0):
                print("MERCI DE M'AVOIR UTILISER")
                break
            if(a==1):
                print("LES INFO VALIDES")
                print(Traiter)
                print("LES INFO INVALIDES")
                print(tabinv)
            elif(a==2):
                id=int(input("donne l'id"))
                print(Traiter[id])
            elif(a==3):
                print(classement[:5])
            elif(a==4):
                print("attendre")
        else:
            print("erreur")
    except Exception as e:
        print("donner invalide")




