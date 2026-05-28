# QHDALABS-RTANA — eksperyment badawczy

## Co to jest?

RTANA to eksperyment badawczy sprawdzający, czy system AI może posiadać
własną, wewnętrzną oś czasu — nie przez dopisanie daty do promptu,
lecz przez architekturę w której kolejne zdarzenia budują historię
wpływającą na przyszłe zachowanie.

Dzisiejsze modele AI działają następująco:

- dostają pytanie
- generują odpowiedź
- „zamierają" do następnego zapytania

Między rozmowami nic się nie dzieje. Nie ma ciągłości, nie ma własnej
historii, nie ma "teraz". Model nie wie czy odpowiada po sekundzie
czy po tygodniu od poprzedniej wymiany.

RTANA bada czy to można zmienić — nie filozoficznie, ale architekturalnie.

---

## Najprostsza intuicja

Zwykły zegar mówi systemowi: „jest godzina 12:03".

RTANA pyta o coś innego:

> Czy system może budować własne „teraz" z tego, co sam przeżył
> krok po kroku — tak żeby przeszłość zmieniała sposób reagowania
> na przyszłość?

Różnica między:

- notatnikiem który tylko zapisuje fakty
- a organizmem którego kolejne doświadczenia zmieniają sposób reagowania

RTANA próbuje zbudować coś bliższego temu drugiemu,
w bardzo ostrożnym, technicznym sensie.

---

## Jak to działa?

System składa się z dwóch części:

**Moduł kwantowy (Qiskit)** — w każdym kroku wykonuje pomiar kubitu.
Wynik pomiaru (0 lub 1) jest "faktem relacyjnym" w sensie fizyki
Carla Rovellego: faktem który istnieje względem obserwatora (kubitu
mierzącego), a nie absolutnie. Sekwencja tych faktów tworzy oś czasu.

**Sieć neuronowa (PyTorch, GRU)** — przechowuje stan ukryty `h(t)`
który aktualizuje się po każdym fakcie relacyjnym. Historia mostów
kwantowych perturbuje Hamiltonian układu. Historia faktów moduluje
fazy kwantowe następnego kroku.

Kluczowa zasada: system nie tylko zapisuje historię — żyje w historii.

```
S(t) → wpływa na generację E(t) → aktualizuje S(t+1)
```

Przeszłość zmienia fizykę następnego kroku.

---

## Co pokazują aktualne wyniki?

Pierwsze wersje systemu miały problem: rule_qubit "zamarzał" w stanie
deterministycznym, wszystkie pomiary dawały to samo, entropia osi czasu
wynosiła 0.

Po poprawkach architektury (przywrócenie superpozycji przed pomiarem,
właściwa kolejność operacji):

**Test pojedynczego przebiegu:**

- 16 kroków relacyjnych z mieszanymi wynikami (0 i 1)
- Entropia osi czasu: ~0.70 bit (bliska idealnemu 1.0)
- J Hamiltoniana dryfuje przez historię mostów (j_drift = 0.06)
- Stan ukryty `||h||` aktywnie ewoluuje przez wszystkie kroki

**Test wrażliwości na historię (kluczowy):**
```
Run 1 — timeline: 0000100011100000
Run 2 — timeline: 0111110000000000
||h1 - h2|| = 2.12
```

Dwie różne historie → dwa różne stany końcowe. Odległość 2.12
w przestrzeni 64-wymiarowej — wyraźna, niemożliwa do przeoczenia.

To oznacza że: historia systemu staje się realnym elementem jego stanu,
a nie tylko zapisanym logiem zdarzeń.

---

## Czym RTANA nie jest

To ważne, bo temat łatwo brzmi bardziej sensacyjnie niż powinien.

RTANA nie zakłada że AI "czuje" czas jak człowiek.
RTANA nie zakłada że system jest świadomy.
RTANA nie jest "lepszą pamięcią" doczepioną do LLM.

Badane jest coś skromniejszego, ale konkretnego:

- czy system może mieć własną sekwencję wewnętrznych zdarzeń
- czy ta sekwencja może wpływać na jego przyszłe zachowanie
- czy da się to zmierzyć eksperymentalnie

Nie pytamy czy maszyna coś przeżywa.
Pytamy czy jej architektura może mieć własną historię działania.

---

## Dlaczego to jest ciekawe?

Większość obecnych modeli AI:

- nie ma własnego "teraz"
- nie posiada ciągłości między zdarzeniami
- działa jedynie reaktywnie — `y = f(x)`

RTANA bada możliwość architektury w której:
`S(t+1) = F(S(t), x, event)`

To nie jest mała zmiana. To jest zmiana klasy systemu — z funkcji
do procesu.

Inspiracją jest fizyka relacyjna Carla Rovellego i formalizm
Page-Woottersa, w których czas wyłania się z relacji między
układami fizycznymi — nie istnieje jako tło, ale jako sekwencja
faktów. Tu próbujemy to samo przenieść do architektury sieci neuronowej.

---

## Stan projektu (maj 2026)

- ✅ Manifesto i formalna specyfikacja napisane
- ✅ Minimalna implementacja `rtana_v1.py` działa
- ✅ Historia różnicuje stany — mechanizm potwierdzony
- ⬜ Testy NIST losowości osi czasu
- ⬜ Skalowanie do większych sieci
- ⬜ Integracja z modelem językowym (Level 2)

Kod i dokumenty: [github.com/QHDALabs/QHDALabs-RTANA](https://github.com/QHDALabs/QHDALabs-RTANA)

---

*Projekt wynika bezpośrednio z wcześniejszych eksperymentów QHDALabs
z kwantowymi mostami i szyfrowaniem relacyjnym (qmnet, RQTE).
Niezależne badania. Bez grantu. Qiskit + PyTorch + za dużo kawy.*