class demo():
    behaviorDict = {}

    def getAction(self, time):
        # Gegeven een tijd geef terug wat deze agent wil doen en hoe belangrijk hij dit vind
        return self.behaviorDict.get(time)

class kind(demo):
    behaviorDict = {"0:00": (100, "slapen"),
                    "9:00": (100, "School"),
                    "12:00": (100, "lunch"),
                    "12:30": (100, "School"),

                    "15:30": [(30, "park"),(20, "recreatie"),(50, "thuis")],

                    "17:00": (100, "Thuis"),
                    "21:00": (100, "slapen")}

    behaviorDict_wk = {
                    "0:00": (100, "slapen"),
                    "9:00": (100, "Thuis"),
                    "12:00": (100, "lunch"),
                    "13:00": [(40, "park"),(40, "recreatie"),(20, "thuis")],
                    
                    "17:00": (100, "Thuis"),
                    "21:00": (100, "slapen")}

class student(demo):
    behaviorDict = {"0:00": (100, "slapen"),
                    "9:00": (100, "School"),
                    "12:00": (100, "lunch"),
                    "12:30": (100, "School"),

                    "15:30": [(10, "park"),(50, "recreatie"),(40, "thuis")],
                    
                    "20:00": (100, "Thuis"),
                    "23:00": (100, "slapen")}

    behaviorDict_wk = {
                    "0:00": (100, "slapen"),
                    "9:00": (100, "Thuis"),
                    "12:00": (100, "lunch"),
                    
                    "13:00": [(5, "park"),(60, "recreatie"),(35, "thuis")],
                    
                    "20:00": (100, "Thuis"),
                    "23:00": (100, "slapen")}

class volwassen_onder_45(demo):
    behaviorDict = {"0:00": (100, "slapen"),
                    "9:00": (100, "Werk"),
                    "12:00": (100, "lunch"),
                    "12:30": (100, "Werk"),

                    "17:30": [(33, "recreatie"),(67, "thuis")],

                    "20:30": (100, "Thuis"),
                    "22:00": (100, "slapen")}

    behaviorDict_wk = {
                    "0:00": (100, "slapen"),
                    "9:00": (100, "Thuis"),
                    "12:00": (100, "lunch"),

                    "13:00": [(25, "park"),(25, "recreatie"),(50, "thuis")],
                    
                    "17:00": (100, "Thuis"),
                    "22:00": (100, "slapen")}

class volwassen_onder_45(demo):
    behaviorDict = {"0:00": (100, "slapen"),

                    "9:00": (100, "Werk"),
                    "12:00": (100, "lunch"),
                    "12:30": (100, "Werk"),

                    "17:30": [(25, "recreatie"),(75, "thuis")],
                    
                    "19:30": (100, "Thuis"),
                    "22:00": (100, "slapen")}

    behaviorDict_wk = {
                    "0:00": (100, "slapen"),
                    "9:00": (100, "Thuis"),
                    "12:00": (100, "lunch"),
                    
                    "13:00": [(30, "park"),(30, "recreatie"),(40, "thuis")],
                    
                    "17:00": (100, "Thuis"),
                    "22:00": (100, "slapen")}


class senioren(demo):
    behaviorDict = {"0:00": (100, "slapen"),
                    "9:30": (100, "thuis"),
                    "12:00": (100, "lunch"),
                    "13:00": [(40, "park"),(30, "recreatie"),(30, "thuis")],

                    "16:30": (100, "Thuis"),
                    "22:00": (100, "slapen")}

    behaviorDict_wk = {
                    "0:00": (100, "slapen"),
                    "9:00": (100, "Thuis"),
                    "12:00": (100, "lunch"),

                    "13:00": [(40, "park"),(40, "recreatie"),(20, "thuis")],
                    
                    "17:00": (100, "Thuis"),
                    "22:00": (100, "slapen")}

class geinfecteerd(demo):
    behaviorDict = {"0:00": (100, "slapen"),
                    "9:00": (100, "Thuis"),
                    "12:00": (100, "lunch"),
                    "19:30": (100, "Thuis"),
                    "21:00": (100, "slapen")}

    behaviorDict_wk = {
                    "0:00": (100, "slapen"),
                    "10:00": (100, "Thuis"),
                    "12:00": (100, "lunch"),
                    "19:30": (100, "Thuis"),
                    "21:00": (100, "slapen")}
