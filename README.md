### **Tim:**

-  Dragana Filipović, SW-47-2018
-  Nikolina Tošić, SW-36-2018

### **Asistent:**

- Dragan Vidaković

### **Definicija problema:**
Na osnovu karata koje se nalaze na talonu, kao i karata koje igrač ima u rukama vrši se njihova detekcija i predviđa se najbolji potez koji igrač može da odigra.

### **Skup podataka:**
Skup podataka ćemo same kreirati, uz korišćenje augmentacije podataka.

### **Metodologija:**
Koristiće se YOLOv3 algoritam (gotov model) za prepoznavanje karata sa slika. Sumiraće se vrednost svake karte, kao i broj karata koje igrač može da pokupi sa talona i analizom toga izračunaće se najbolji potez. Posebnim kartama će biti dodeljena veća vrednost.

### **Evaluacija:**
Za klasifikaciju, kao i evaluaciju detekcije karata koristiće se accuracy. Koristiće se IoU metrika.

