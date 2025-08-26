- Der Gesamte Bot muss in einer Pythin file geschrieben werden
- Der Name des Bots sollte mit __bot__ beginnen
- Der Bot muss eine __start__ und eine __step__ funktion erhalten
- Jede Form des State muss in __start__ initialisiert werden. Dies sorgt dafür, dass Bots mehfach hintereinander gegeneinander spielen können, ohne den kompletten Namespace neu laden zu müssen
- Die __start__ funktion besitzt folgenden Syntax:
'''
def start(team):
  ...
  return None #can be implicid
'''
- Die __step__ funktion besitzt folgenden Syntax:
'''
def step(board):
  ...
  return move
'''
- Dieser Move besitzt folgenden Syntax:
  - Der Ursprung befindet sich links oben
  - __PS;(x,y)__ um einen Stein an der Position x(Spalte), y(Zeile)
  - __PW;(x,y)__ um eine Wand zu platzieren
  - __PC;(x,y)__ um einen Capstone zu plazieren
  - __MO;(x,y);D;(C,...)__ um Steine in Richtung '''{N,W,S,E}''' zu bewegen. Nach dem Ursprungsstein werden __C__ Steine Abgeworfen
