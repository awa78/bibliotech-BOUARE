# BiblioTech v1.3
# gestion de la bibliotheque municipale
# auteur : stagiaire 2019, modifie par plusieurs personnes depuis
import logging
import os
import sys
from datetime import date, datetime, timedelta

# Règles métier : durées en jours, pénalités en euros par jour de retard.
LOAN_DAYS = {"book": 21, "dvd": 7, "magazine": 3}
DAILY_FEE = {"book": 0.5, "dvd": 1.0, "magazine": 0.2}
MAX_LOANS = {"standard": 3, "student": 5, "premium": 8}
LOGGER = logging.getLogger(__name__)

DATA = os.environ.get("BIBLIOTECH_DATA", "data")
TODAY = None
debug = False
cache = {}
def late_fee(
    days_late: int, kind: str, member_type: str, price: float
) -> float:
    """Pénalité de retard, réduite selon le membre et plafonnée au prix."""
    if days_late <= 0:
        return 0.0

    fee = days_late * DAILY_FEE.get(kind, DAILY_FEE["book"])

    if member_type == "student":
        fee *= 0.5
    elif member_type == "premium":
        fee = 0.0

    return round(min(fee, price), 2)



class Library:
    def __init__(self):
        self.b = []
        self.m = []
        self.l = []
        self.plugins = {}
        self.load()

    # chargement des donnees
    def load(self):
        """Charger les trois CSV sans exécuter leur contenu."""
        with open(DATA + "/books.csv") as f:
            lines = f.readlines()
        for line in lines[1:]:
            if line.strip() == "":
                continue
            x = line.strip().split(";")
            self.b.append(
                {
                    "id": x[0],
                    "title": x[1],
                    "author": x[2],
                    "kind": x[3],
                    # Un prix doit être numérique : ne jamais utiliser eval ici.
                    "price": float(x[4]),
                    "copies": int(x[5]),
                }
            )
        with open(DATA + "/members.csv") as f:
            lines = f.readlines()
        for line in lines[1:]:
            if line.strip() == "":
                continue
            x = line.strip().split(";")
            a = x[4] == "1"
            self.m.append(
                {"id": x[0], "name": x[1], "email": x[2], "type": x[3], "active": a}
            )
        with open(DATA + "/loans.csv") as f:
            lines = f.readlines()
        for line in lines[1:]:
            if line.strip() == "":
                continue
            x = line.strip().split(";")
            try:
                fee = float(x[6])
            except (ValueError, IndexError):
                fee = 0
            self.l.append(
                {
                    "id": x[0],
                    "member": x[1],
                    "book": x[2],
                    "start": x[3],
                    "due": x[4],
                    "returned": x[5],
                    "fee": fee,
                }
            )
        if debug:
            print("chargement ok", len(self.b), len(self.m), len(self.l))

    def save(self):
        with open(DATA + "/loans.csv", "w") as f:
            f.write("id;member_id;book_id;start;due;returned;fee\n")
            for x in self.l:
                f.write(
                    ";".join(
                        [
                            x["id"],
                            x["member"],
                            x["book"],
                            x["start"],
                            x["due"],
                            x["returned"],
                            f"{x['fee']:.2f}",
                        ]
                    )
                    + "\n"
                )

    # t = "b" pour livre, "m" pour membre, "l" pour emprunt
    def find(self, t, id):
        if t == "b":
            for x in self.b:
                if x["id"] == id:
                    return x
        elif t == "m":
            for x in self.m:
                if x["id"] == id:
                    return x
        elif t == "l":
            for x in self.l:
                if x["id"] == id:
                    return x
        return None

    def count_active_loans(self, mid):
        n = 0
        for x in self.l:
            if x["member"] == mid and x["returned"] == "":
                n = n + 1
        return n

    def dispo(self, bid):
        bk = self.find("b", bid)
        n = 0
        for x in self.l:
            if x["book"] == bid and x["returned"] == "":
                n = n + 1
        return bk["copies"] - n
    def has_overdue_loan(self, member_id):
        return any(
            loan["member"] == member_id
            and loan["returned"] == ""
            and datetime.strptime(loan["due"], "%Y-%m-%d").date() < get_today()
            for loan in self.l
        )
    def is_borrowing(self, member_id, book_id):
        return any(
            loan["member"] == member_id
            and loan["book"] == book_id
            and loan["returned"] == ""
            for loan in self.l
        )
    def refusal_reason(self, member, book):
        if not member["active"]:
            return "membre inactif"

        if self.has_overdue_loan(member["id"]):
            return "emprunts en retard"

        limit = MAX_LOANS.get(member["type"], MAX_LOANS["standard"])
        if self.count_active_loans(member["id"]) >= limit:
            return f"limite d'emprunts atteinte ({limit})"

        if self.is_borrowing(member["id"], book["id"]):
            return "deja emprunte par ce membre"

        if self.dispo(book["id"]) <= 0:
            return "plus d'exemplaire disponible"

        return None
    def create_loan(self, member, book):
        days = LOAN_DAYS.get(book["kind"], LOAN_DAYS["book"])
        today = get_today()
        due = today + timedelta(days=days)

        max_id = 0
        for loan in self.l:
            number = int(loan["id"][1:])
            if number > max_id:
                max_id = number

        new_id = "L" + str(max_id + 1).zfill(3)
        self.l.append(
            {
                "id": new_id,
                "member": member["id"],
                "book": book["id"],
                "start": str(today),
                "due": str(due),
                "returned": "",
                "fee": 0,
            }
        )
        self.save()
        print(
            f"Emprunt {new_id} enregistre : {book['title']} "
            f"pour {member['name']}, retour avant le {due}"
        )

    # emprunter un document
    def borrow (self, member_id, book_id):
        member = self.find("m", member_id)
        if member is None:
            print("Erreur : membre inconnu")
            return False

        book = self.find("b", book_id)
        if book is None:
            print("Erreur : livre inconnu")
            return False

        reason = self.refusal_reason(member, book)
        if reason is not None:
            print(f"Refus : {reason}")
            return False

        self.create_loan(member, book)
        return True

    # retour d'un document
    def ret(self, lid):
        ln = self.find("l", lid)
        if ln is None:
            print("Erreur : emprunt inconnu")
            return
        if ln["returned"] != "":
            print("Erreur : emprunt deja rendu")
            return
        bk = self.find("b", ln["book"])
        mb = self.find("m", ln["member"])
        t = get_today()
        d = (t - datetime.strptime(ln["due"], "%Y-%m-%d").date()).days
        if d < 0:
            d = 0
        f = late_fee(d, bk["kind"], mb["type"], bk["price"])
        ln["returned"] = str(t)
        ln["fee"] = f
        self.save()
        print(
            f"Retour enregistre : {bk['title']}. Retard : {d} jour(s). "
            f"Penalite : {f:.2f} EUR"
        )

    # liste des retards + envoi des rappels
    def overdue(self):
        tmp = []
        for x in self.l:
            if (
                x["returned"] == ""
                and datetime.strptime(x["due"], "%Y-%m-%d").date() < get_today()
            ):
                tmp.append(x)
        if len(tmp) == 0:
            print("Aucun retard.")
            return
        tmp.sort(key=lambda x: (x["due"], x["id"]))
        total = 0
        for x in tmp:
            book = self.find("b", x["book"])
            member = self.find("m", x["member"])
            nbj = (get_today() - datetime.strptime(x["due"], "%Y-%m-%d").date()).days
            # calcul penalite
            p = late_fee(nbj, book["kind"], member["type"], book["price"])
            total = total + p
            print(
                f"{x['id']} | {member['name']} | {book['title']} | "
                f"{nbj} jour(s) | {p:.2f} EUR"
            )
            # envoi du mail
            print(
                f"EMAIL -> {member['email']} : Rappel, vous devez rendre "
                f"'{book['title']}' (retard {nbj} jours)"
            )
        print("Total des penalites en cours : " + "%.2f" % total + " EUR")

    def report(self):
        data2 = {}
        print("=== RAPPORT BIBLIOTECH ===")
        print("Date : " + str(get_today()))
        c = 0
        for x in self.b:
            c = c + x["copies"]
        print("Titres : " + str(len(self.b)) + " (" + str(c) + " exemplaires)")
        a = 0
        for x in self.m:
            if x["active"]:
                a = a + 1
        print("Membres : " + str(len(self.m)) + " dont " + str(a) + " actifs")
        en_cours = 0
        en_retard = 0
        encaisse = 0
        a_payer = 0
        for x in self.l:
            if x["returned"] == "":
                en_cours = en_cours + 1
                due = datetime.strptime(x["due"], "%Y-%m-%d").date()
                if due < get_today():
                    en_retard = en_retard + 1
                    bk = self.find("b", x["book"])
                    mb = self.find("m", x["member"])
                    j = (get_today() - due).days
                    pen = late_fee(j, bk["kind"], mb["type"], bk["price"])
                    a_payer = a_payer + pen
            else:
                encaisse = encaisse + x["fee"]
            if x["book"] in data2:
                data2[x["book"]] = data2[x["book"]] + 1
            else:
                data2[x["book"]] = 1
        print(
            f"Emprunts : {len(self.l)} au total, {en_cours} en cours, "
            f"{en_retard} en retard"
        )
        print("Penalites encaissees : " + "%.2f" % encaisse + " EUR")
        print("Penalites en attente : " + "%.2f" % a_payer + " EUR")
        # par type
        k = {}
        for x in self.l:
            bk = self.find("b", x["book"])
            if bk["kind"] in k:
                k[bk["kind"]] += 1
            else:
                k[bk["kind"]] = 1
        for kk in sorted(k.keys()):
            print("  - " + kk + " : " + str(k[kk]) + " emprunt(s)")
        # top 3
        lst = []
        for key in data2:
            lst.append((-data2[key], self.find("b", key)["title"]))
        lst.sort()
        print("Top 3 :")
        i = 0
        for x in lst:
            if i < 3:
                print("  " + str(i + 1) + ". " + x[1] + " (" + str(-x[0]) + ")")
            i = i + 1

    def export(self, fname, sep):
        with open(fname, "w") as f:
            f.write(
                sep.join(
                    [
                        "loan_id",
                        "member",
                        "title",
                        "start",
                        "due",
                        "returned",
                        "days_late",
                        "fee",
                    ]
                )
                + "\n"
            )
            n = 0
            for x in self.l:
                bk = self.find("b", x["book"])
                mb = self.find("m", x["member"])
                if x["returned"] != "":
                    end = datetime.strptime(x["returned"], "%Y-%m-%d").date()
                else:
                    end = get_today()
                dl = (end - datetime.strptime(x["due"], "%Y-%m-%d").date()).days
                if dl < 0:
                    dl = 0
                fee = late_fee(dl, bk["kind"], mb["type"], bk["price"])
                f.write(
                    sep.join(
                        [
                            x["id"],
                            mb["name"],
                            bk["title"],
                            x["start"],
                            x["due"],
                            x["returned"],
                            str(dl),
                            f"{fee:.2f}",
                        ]
                    )
                    + "\n"
                )
                n = n + 1

        print("Export termine : " + str(n) + " lignes dans " + fname)

    # systeme de plugins (pour plus tard)
    def register_plugin(self, name, fn, priority=0, options=None):
        # Créer un dictionnaire distinct pour chaque appel sans options.
        if options is None:
            options = {}
        self.plugins[name] = {"fn": fn, "priority": priority, "options": options}

    def run_plugins(self, event, payload=None):
        """Exécuter les plugins par priorité et journaliser leurs erreurs."""
        res = []
        for name in sorted(self.plugins, key=lambda n: self.plugins[n]["priority"]):
            try:
                res.append(
                    self.plugins[name]["fn"](
                        event, payload, **self.plugins[name]["options"]
                    )
                )
            except Exception:
                # Garder la trace complète ; Ctrl+C et SystemExit restent propagés.
                LOGGER.exception("Echec du plugin %s pour l'evenement %s", name, event)
        return res


def get_today():
    global TODAY
    if TODAY is None:
        return date.today()
    return TODAY


# ancienne version du calcul, ne plus utiliser
def old_calc_fee(days, kind):
    if kind == "book":
        return days * 0.3
    return days * 0.8

def display_catalog(library):
    for book in library.b:
        available = library.dispo(book["id"])
        print(
            f"{book['id']} | {book['title']} | {book['author']} | "
            f"{book['kind']} | {available}/{book['copies']} disponible(s)"
        )

def display_members(library):
    for member in library.m:
        status = "actif" if member["active"] else "inactif"
        print(
            f"{member['id']} | {member['name']} | {member['type']} | "
            f"{status} | {library.count_active_loans(member['id'])} "
            "emprunt(s) en cours"
        )
def handle_borrow(library, args):
    if len(args) < 3:
        print("Usage : borrow <id_membre> <id_document>")
        return 1

    accepted = library.borrow(args[1], args[2])
    if not accepted:
        return 2

    return 0



def process(args):
    global TODAY
    lib = Library()
    if len(args) == 0:
        print(
            "Usage : python bibliotech.py <commande> [arguments] [--today AAAA-MM-JJ]"
        )
        print("Commandes : list, members, borrow, return, overdue, report, export")
        return 1
    cmd = args[0]
    if cmd == "list":
        display_catalog(lib)
    elif cmd == "members":
        display_members(lib)
    elif cmd == "borrow":
        return handle_borrow(lib, args)
    elif cmd == "return":
        if len(args) < 2:
            print("Usage : return <id_emprunt>")
            return 1
        lib.ret(args[1])
    elif cmd == "overdue":
        lib.overdue()
    elif cmd == "report":
        lib.report()
    elif cmd == "export":
        if len(args) < 2:
            print("Usage : export <fichier.csv>")
            return 1
        lib.export(args[1], ";")
    else:
        print("Commande inconnue : " + cmd)
        return 1
    return 0


if __name__ == "__main__":
    a = sys.argv[1:]
    if "--today" in a:
        i = a.index("--today")
        TODAY = datetime.strptime(a[i + 1], "%Y-%m-%d").date()
        a = a[:i] + a[i + 2 :]
    if "--debug" in a:
        debug = True
        a.remove("--debug")
    sys.exit(process(a))
