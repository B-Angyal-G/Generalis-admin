# Generalis-admin
Beosztásgeneráló SBO adminisztrátoroknak.

Rövid ismertető XLSX kérések megadásához:
x  : adott napon sem nappalos, sem éjszakás, sem lelépős nem lehet
y  : adott napon sem nappalos, sem éjszakás nem lehet
nx : adott napon nem lehet nappalos, sem lelépős
ex : adott napon nem lehet éjszakás

Kérések megadásánál kis- és nagy betű nem számít, továbbá 'e'-t és 'é'-t is lehet írni. Valamint 'nx' helyett 'xn'-et is, ugyanígy éjszakáshoz.

Legfontosabb mező, hogy az adott hónap hány napos, valamint, hogy kinek mennyi nappalos illetve éjszakás műszakja legyen (lehet 0 is).
Szükséges még az első szombat megadása, mert beleszámít az értékelésbe.
Fehér C1 és C2 mezőben csak az ellenőrzést megkönnyítő számadatok vannak, melyek a nappalos ill. éjszakás műszakok összegét tartalmazzák. A program nem veszi őket figyelembe.
