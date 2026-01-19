import numpy as np # biblioteka do operacji matematycznych i macierzy.
import matplotlib.pyplot as plt #biblioteka do rysowania wykresów i animacji.
from matplotlib.animation import FuncAnimation #funkcja z Matplotlib, która pozwala tworzyć animacje poprzez aktualizowanie wykresu w czasie.

# ---------------------------------------
# PARAMETRY SYMULACJI
# ---------------------------------------
N = 80                     # liczba agentów
SPEED_LIMIT = 0.05         # maksymalna prędkość agenta
FORCE_GOAL = 0.015         # siła podążania za celem
FORCE_REPULSION = 0.03     # siła odpychania agentów
MIN_DISTANCE = 0.35        # minimalna odległość agentów
AREA_X = (0, 10)           # obszar x
AREA_Y = (0, 10)           # obszar y

# ---------------------------------------
# DANE STARTOWE
# ---------------------------------------
positions = np.random.rand(N, 2) * 10 
#Wszystkie liczby w tej tablicy są losowe i pochodzą z rozkładu jednostajnego w przedziale [0, 1).
#Dlaczego 0–1? Bo to jest standardowy, domyślny rozkład jednostajny w NumPy.
'''
[[0.12, 0.88],
[0.75, 0.34],
... 78 więcej wierszy ...]
'''


velocities = np.zeros((N, 2))
#Tworzy tablicę o wymiarach N x 2 wypełnioną zerami.



# domyślna pozycja myszy (środek)
mouse_position = np.array([5.0, 5.0])

# ---------------------------------------
# OBSŁUGA MYSZY – dynamiczny cel
# ---------------------------------------
def on_move(event):
    global mouse_position
    if event.xdata is not None and event.ydata is not None:
        mouse_position = np.array([event.xdata, event.ydata])

# ---------------------------------------
# ANIMACJA
# ---------------------------------------
fig, ax = plt.subplots()
'''
plt.subplots() – wbudowana funkcja Matplotlib, która tworzy okno wykresu i oś do rysowania.
Zwraca dwie rzeczy:
fig – obiekt figury (okno/plan wykresu).
ax – obiekt osi (miejsce, gdzie rysujemy punkty, linie itp.).
Dzięki temu możemy później rysować agentów w ax i ustawiać granice pola.
'''

fig.canvas.mpl_connect("motion_notify_event", on_move)
'''
fig.canvas – część figury odpowiadająca za interakcję (mysz, kliknięcia).
mpl_connect() – metoda, która podłącza zdarzenie do funkcji.
"motion_notify_event" – wbudowane zdarzenie w Matplotlib → oznacza ruch myszy nad wykresem.
on_move – funkcja, która zostanie wywołana przy tym zdarzeniu.
'''



def update(frame):
    global positions, velocities #Funkcja będzie modyfikować tablice positions i velocities, które są zdefiniowane na zewnątrz. Bez global Python stworzyłby lokalne zmienne, a zmiany nie wpływałyby na animację.

    ax.cla()    #czyści poprzednią klatkę wykresu, żeby narysować nową.
    ax.set_xlim(*AREA_X)    
    ax.set_ylim(*AREA_Y)    #ustawiają granice pola w osi x i y.
    ax.set_aspect("equal")    #sprawia, że jednostki osi x i y są równe, więc ruch agentów nie jest zniekształcony.

    # --- SIŁA PODĄŻANIA ZA CELEM (mysz) ---
    direction_to_goal = mouse_position - positions    #Oblicza wektor od każdego agenta do myszy [dx, dy]
    distance = np.linalg.norm(direction_to_goal, axis=1).reshape(-1, 1)    #Liczy długość wektora (odległość od celu) dla każdego agenta.
    direction_to_goal = direction_to_goal / (distance + 1e-8)    #Normalizuje wektor, żeby mieć jednostkowy kierunek w stronę myszy.
    goal_force = direction_to_goal * FORCE_GOAL    #Mnoży jednostkowy kierunek przez siłę przyciągania → wektor siły, który będziemy dodawać do prędkości agenta.

    # --- SIŁA ODPYCHANIA OD INNYCH AGENTÓW ---
    repulsion = np.zeros((N, 2))    #przygotowujemy tablicę sił odpychających dla wszystkich agentów.
    for i in range(N):    #
        diff = positions[i] - positions    #wektor od wszystkich agentów do agenta i.
        dist = np.linalg.norm(diff, axis=1).reshape(-1, 1)    #odległości od wszystkich agentów.

        close = (dist < MIN_DISTANCE) & (dist > 0)    #sprawdzamy, którzy agenci są za blisko (ignorujemy samego siebie).
        force = (diff / (dist + 1e-8)) * close * FORCE_REPULSION    #oblicza siłę odpychającą od bliskich agentów.
        repulsion[i] = np.sum(force, axis=0)    #sumuje wszystkie siły dla agenta i.

    # --- AKTUALIZACJA PRĘDKOŚCI ---
    velocities += goal_force + repulsion

    # limit prędkości
    speed = np.linalg.norm(velocities, axis=1)
    too_fast = speed > SPEED_LIMIT
    velocities[too_fast] = (velocities[too_fast].T * (SPEED_LIMIT / speed[too_fast])).T

    # --- AKTUALIZACJA POZYCJI ---
    positions += velocities

    # --- RYSOWANIE ---
    ax.scatter(positions[:, 0], positions[:, 1], color="royalblue", s=30)
    ax.scatter(mouse_position[0], mouse_position[1], color="red", s=80, marker="X")

    ax.set_title("Symulacja tłumu – agenci podążają za myszką")

# UWAGA USUNIĘTA – cache_frame_data=False
ani = FuncAnimation(fig, update, interval=30)
plt.show()
