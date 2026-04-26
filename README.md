# OOP Kursinis darbas: PING PONG žaidimas
---

## 1. Įvadas
Šio projekto tikslas – sukurti „Ping Pong“ žaidimą naudojant Python programavimo kalbą kartu su pygame biblioteką, pritaikant objektinio  programavimo (OOP) principus. Programa leidžia žaidėjui valdyti raketę, atmušinėti kamuoliuką bei taip rinkti taškus ir varžytis su draugais.  Vėliau rezultatai yra išsaugomi atskirame .csv faile, o po kiekvieno žaidimo sistema praneš apie laimėtoją, surinktų taškų kraitį bei  viršutiniame dešiniajame kampe bus atvaizduojamas didžiausias taškų skirtumas.
---

## 2. Analizė

Projekte panaudoti visi keturi pagrindiniai OOP principai

### 2.1. Abstrakcija (Abstraction)
Sukurta bazinė abstrakti klasė **GameObject**. Ji nurodo, kad visi žaidimo objektai privalo turėti (pvz.:**update()**) metodą, tačiau pati jo  neįgyvendina.  

[Abstrakcijos pavyzdys kode](abstrakcija.png) 

### 2.2. Paveldėjimas (Inheritance)
Klasės **Ball**, **Paddle** ir **GoldenPoint** paveldi savybes iš **GameObject**. Tai leidžia išvengti kodo dubliavimo ir logiškai suskirstyti objektus pagal jų paskirtį. 

[Paveldėjimo kamuoliuko pavyzdys kode](paveldejimasBALL.png)  
[Paveldėjimo raketės pavyzdys kode](paveldejimasPADDLE.png) 

### 2.3. Polimorfizmas (Polymorphism)
Nors visi objektai turi **update()** metodą, kiekviena klasė jį įgyvendina skirtingai:
- **Ball** klasėje jis skaičiuoja judėjimo trajektoriją.
- **Paddle** klasėje jis valdo raketės poziciją pagal žaidėjo klavišų paspaudimus. 

[Polimorfizmo raketės pavyzdys kode](update()PADDLE.Polimorfizmas.png)  
[Polimorfizmo kamuoliuko pavyzdys kode](update()BALL.Polimorfizmas.png)


### 2.4. Inkapsuliacija (Encapsulation)
Objektų būsenos valdomos naudojant apsaugotus atributus (pvz., **_rect**). Duomenys apie objektų koordinates ir greitį nėra tiesiogiai pasiekiami iš išorės, o valdomos per tam skirtus metodus. 

[Inkapsuliacijos pavyzdys kode](inkapsuliacija.png)


### 2.5. Kompozicija
**GameManager** klasė naudoja **kompoziciją** – ji savo viduje sukuria ir valdo **Ball** bei **Paddle** objektus. Jei sunaikintume  **GameManager**, tai dingtų ir **Ball** bei **Paddle** objektai sukurti to GameManager.

---

## 3. Dizaino šablonas (Design Pattern)

Projekte pritaikytas **Singleton** dizaino šablonas **GameManager** klasei. 
- **Pasirinkimo priežastis:** Žaidime gali būti tik vienas pagrindinis "bosas", atsakingas už lango kūrimą, taškų skaičiavimą ir pagrindinį  ciklą. Kitais atvejais atsirastų galimybė, jog vienu metu galėtume būti atidaryti keli skirtingi žaidimo langai.
- **Įgyvendinimas:** Naudojamas **__new__** metodas, kuris užtikrina, kad sukūrus kelis **GameManager()**, jie visi rodytų į tą patį objektą atmintyje.

---

## 4. Darbas su failais

Programa pilnai įgyvendina duomenų rašymą ir skaitymą:
* **Rašymas:** Pasibaigus žaidimui, žaidėjo vardas (RED or BLUE) ir surinkti taškai įrašomi į **scores.csv** failą.
* **Skaitymas:** Funkcija **load_high_score** **scores.csv** faile surandą didžiausią taškų skirtumą ir jį atvaizduoja žaidimo pabaigos lange.

---

## 5. Testavimas (unittesting)

Naudojant **unittest** šabloną, sukurti testai faile **test_PONG.py**, kurie patikrina:
- Ar kamuoliuko **reset()** funkcija teisingai grąžina jį į pradinę poziciją.
- Ar kamuoliuko greitis neviršija nustatytų limitų.
- Ar **GameManager** klasė tikrai veikia kaip Singleton.

---

## 6. Rezultatai ir Išvados

**Rezultatai:**
- Sukurta veikianti žaidimo versija.
- Įgyvendinta taškų sistema ir jų saugojimas atskirame faile.
- Kodas yra lengvai plečiamas (pvz., pridedant naujų tipų/kamuoliuko efektų).

**Išvados:**
Pavyko sukurti tvarkingą ir lengvai skaitomą kodą. Singleton šablonas puikiai integruotas, o jame taip pat galime įžvelgti ir **state** šablono užuominų. (**unittest**) leidžia patikrinti, kad keičiant kodo dalis, žaidimas neprarastų svarbių funkcijų. Didžiausias iššūkis buvo integruoti **state** šablono dalis į Singleton kodo dalį. Tačiau būtent tai ir privedė prie aiškaus dizaino.
