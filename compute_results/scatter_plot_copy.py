import matplotlib.pyplot as plt
import numpy as np

# Dados de exemplo
x = np.random.rand(50)
y = np.random.rand(50)

# Criando uma figura e eixos para os gráficos
fig, axs = plt.subplots(2, 3, figsize=(12, 8))

# Gráficos na parte de cima
axs[0, 0].scatter(x, y)
axs[0, 0].set_title('Plot 1')

axs[0, 1].scatter(x, y, color='orange')
axs[0, 1].set_title('Plot 2')

axs[0, 2].scatter(x, y, color='green')
axs[0, 2].set_title('Plot 3')

# Gráficos na parte de baixo
axs[1, 0].scatter(x, y, color='red')
axs[1, 0].set_title('Plot 4')

axs[1, 1].scatter(x, y, color='purple')
axs[1, 1].set_title('Plot 5')

axs[1, 2].scatter(x, y, color='blue')
axs[1, 2].set_title('Plot 6')

# Ajustando layout
plt.tight_layout()

# Mostrando os gráficos
plt.show()
