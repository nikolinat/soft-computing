### **Tim:**

-  Dragana Filipović, SW-47-2018
-  Nikolina Tošić, SW-36-2018

### **Asistent:**

- Dragan Vidaković

### **Definicija problema:**
Na osnovu karata koje se nalaze na talonu, kao i karata koje igrač ima u rukama vrši se njihova detekcija i predviđa se najbolji potez koji igrač može da odigra.

### **Skup podataka:**
[Ručno generisan skup podataka](https://drive.google.com/drive/folders/1j8h9UmSly1tQZp4QUYM_uCsIHPXX3hPr?usp=sharing) 
<br>[Testni skup podataka](https://drive.google.com/drive/folders/1aFQd15G6MJiHladOY2nygqTxYSXkOYy0?usp=sharing)
<br>Augmentacija nad podacima je vršena pomoću Jupyter Notebook-a, uz imgaug biblioteku, skripta se nalazi u okviru projekta.

### **Metodologija:**
Korišćen je YOLOv3 algoritam (gotov model) za prepoznavanje karata sa slika, koji se nalazi na sledećem linku https://github.com/AntonMu/TrainYourOwnYOLO
<br>Heuristika je ručno implementirana, najbolji potez je izabran na osnovu sume prioriteta karata gde posebne karte imaju veći prioritet.

### **Treniranje:**
[Skripta za treniranje na Google Colab-u](https://drive.google.com/drive/folders/124VxRqueR4Ne_e6CEvCcSGvmHO5vOSrv?usp=sharing)

### **Pokretanje:**
Za korišćenje projekta potrebna je python verzija 3.6 ili 3.7, pored navedenog treba instalirati sve iz requirements.txt komandom pip install -r requirements.txt. 
<br>[Težine](https://drive.google.com/drive/folders/124VxRqueR4Ne_e6CEvCcSGvmHO5vOSrv?usp=sharing) je potrebno ubaciti u model_data.
Komandom python main.py pokreće se detektovanje i određivanje najboljeg poteza za dve slučajno odabrane karte iz test foldera.
Za evaluaciju i detekciju karata se koristi detector.py koji se pokreće komandom detector.py iz src foldera.

### **Evaluacija:**
Prikazani podaci su rezultati testiranja na gore navedenom skupu.

| F1 score  | Recall | Precision | Accuracy 
| ------------- | ------------- |-------------| -------------
|     97      |  98.19 | 95.84 | 94.18

