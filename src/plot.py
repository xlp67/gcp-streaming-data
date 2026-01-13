import matplotlib.pyplot as plt
from collections import deque
import time  # <--- IMPORTANTE: Importar a biblioteca de tempo

class RealTimePlotter:
    def __init__(self, max_len=100, title="Dados do Sensor em Tempo Real"):
        self.max_len = max_len
        
        # Buffers
        self.data_x = deque(maxlen=max_len)
        self.data_y = deque(maxlen=max_len)
        self.data_z = deque(maxlen=max_len)
        self.indexes = deque(maxlen=max_len)
        self.counter = 0

        # --- CORREÇÃO AQUI ---
        # Inicializa o tempo de início para calcular a frequência
        self.start_time = time.time()  
        # ---------------------

        # Configuração do gráfico
        plt.ion()
        self.fig, self.ax = plt.subplots()
        self.fig.canvas.manager.set_window_title(title)
        
        # Inicialização das linhas
        self.line_x, = self.ax.plot([], [], 'r-', label='X')
        self.line_y, = self.ax.plot([], [], 'g-', label='Y')
        self.line_z, = self.ax.plot([], [], 'b-', label='Z')
        
        # Texto na tela
        self.info_text = self.ax.text(0.02, 0.95, '', transform=self.ax.transAxes, 
                                      verticalalignment='top', bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
        
        self.ax.set_ylim(-20, 20)
        self.ax.legend(loc='upper left')
        self.ax.grid(True)
        self.ax.set_xlabel("Amostras")
        self.ax.set_ylabel("Valor")

    def update(self, x, y, z, isPass):
        """Atualiza o gráfico com novos valores."""

        if isPass:
            print(isPass)
            self.counter += 1
        
        # Adiciona dados aos buffers
        self.indexes.append(self.counter)
        self.data_x.append(x)
        self.data_y.append(y)
        self.data_z.append(z)

        # Atualiza os dados das linhas
        self.line_x.set_data(self.indexes, self.data_x)
        self.line_y.set_data(self.indexes, self.data_y)
        self.line_z.set_data(self.indexes, self.data_z)

        # Ajusta os limites do eixo X
        self.ax.set_xlim(self.indexes[0], self.indexes[-1] + 1)
       
        # --- CÁLCULO DE FREQUÊNCIA ---
        current_time = time.time()
        # Agora self.start_time existe, então não dará erro
        elapsed_time = current_time - self.start_time
        steps_per_sec = 0.0
        
        if elapsed_time > 0:
            steps_per_sec = self.counter / elapsed_time

        # Atualiza o texto
        self.info_text.set_text(f"Passos: {self.counter}\nFreq: {steps_per_sec:.2f} /s")

        # Redesenha o canvas
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()
        
    def close(self):
        plt.ioff()
        plt.show()