import numpy as np
import matplotlib.pyplot as plt

# Symulacja danych na podstawie parametrów Twojego projektu
density = np.linspace(0.1, 1.5, 100)
# Modelowanie spadku prędkości przy wzroście zagęszczenia (zgodnie z wynikami projektu)
# Prędkość maksymalna to Twoje SPEED_LIMIT = 0.05
speed_limit = 0.05
speed = speed_limit * np.exp(-1.2 * (density - 0.1)) 

plt.figure(figsize=(10, 6))
plt.plot(density, speed, color='royalblue', linewidth=3, label='Prędkość grupy')
plt.fill_between(density, speed, alpha=0.2, color='royalblue')

# Dodanie punktów kontrolnych odpowiadających zachowaniu agentów
plt.scatter([0.2, 0.8, 1.3], [0.045, 0.022, 0.012], color='red', zorder=5)
plt.annotate('Ruch swobodny', xy=(0.2, 0.045), xytext=(0.4, 0.048), arrowprops=dict(arrowstyle='->'))
plt.annotate('Zwiększone odpychanie', xy=(0.8, 0.022), xytext=(1.0, 0.030), arrowprops=dict(arrowstyle='->'))

# Formatowanie wykresu
plt.title('Diagram Fundamentalny: Prędkość vs Zagęszczenie w symulacji', fontsize=14, pad=20)
plt.xlabel('Zagęszczenie (liczba agentów na jednostkę powierzchni)', fontsize=12)
plt.ylabel('Średnia prędkość (j/krok)', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.6)
plt.ylim(0, 0.06)
plt.legend()

plt.tight_layout()
plt.show()