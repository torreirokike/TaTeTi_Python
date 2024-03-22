import tkinter as tk
from tkinter import messagebox
import random

class TicTacToe(tk.Tk):
    def __init__(self):
        """
        Inicialización de la aplicación.
        """
        super().__init__()
        self.title("Tateti")
        self.geometry("300x350")
        self.current_player = "X"  # Jugador actual
        self.board = [[" " for _ in range(3)] for _ in range(3)]  # Tablero de juego
        self.player_symbol = "X"  # Símbolo del jugador humano
        self.computer_symbol = "O"  # Símbolo de la consola
        self.player_wins = 0  # Contador de victorias del jugador
        self.computer_wins = 0  # Contador de victorias de la consola

        self.create_widgets()  # Crear widgets de la interfaz gráfica

    def create_widgets(self):
        """
        Crea los widgets de la interfaz gráfica.
        """
        self.buttons = []
        for i in range(3):
            row = []
            for j in range(3):
                button = tk.Button(self, text=" ", font=("Arial", 20), width=3, height=1,
                                   command=lambda i=i, j=j: self.make_move(i, j))
                button.grid(row=i, column=j, padx=5, pady=5)
                row.append(button)
            self.buttons.append(row)

        # Etiquetas para mostrar el contador de victorias
        self.player_label = tk.Label(self, text=f"Jugador: {self.player_wins}", font=("Arial", 12))
        self.player_label.grid(row=3, column=0, columnspan=1, padx=5, pady=5)  # Ajuste aquí

        self.computer_label = tk.Label(self, text=f"Consola: {self.computer_wins}", font=("Arial", 12))
        self.computer_label.grid(row=3, column=1, columnspan=2, padx=5, pady=5)

    def make_move(self, row, col):
        """
        Realiza el movimiento del jugador actual y comprueba el resultado del juego.
        """
        if self.board[row][col] == " ":
            self.board[row][col] = self.player_symbol
            self.buttons[row][col].config(text=self.player_symbol, state="disabled")
            if self.check_winner(self.player_symbol):
                messagebox.showinfo("Tateti", "¡Ganaste!")
                self.player_wins += 1
                self.reset_board()
                return
            if self.check_draw():
                messagebox.showinfo("Tateti", "¡Empate!")
                self.reset_board()
                return
            self.computer_move()

    def computer_move(self):
        """
        Realiza el movimiento de la consola y comprueba el resultado del juego.
        """
        empty_cells = [(i, j) for i in range(3) for j in range(3) if self.board[i][j] == " "]
        if empty_cells:
            row, col = self.get_best_move(empty_cells)  # Obtener el mejor movimiento
            self.board[row][col] = self.computer_symbol
            self.buttons[row][col].config(text=self.computer_symbol, state="disabled")
            if self.check_winner(self.computer_symbol):
                messagebox.showinfo("Tateti", "¡La consola gana!")
                self.computer_wins += 1
                self.reset_board()
                return
            if self.check_draw():
                messagebox.showinfo("Tateti", "¡Empate!")
                self.reset_board()

    def get_best_move(self, empty_cells):
        """
        Obtiene el mejor movimiento para la consola para evitar que el jugador gane.
        """
        # Verificar si la consola puede ganar en el siguiente movimiento
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == " ":
                    self.board[i][j] = self.computer_symbol
                    if self.check_winner(self.computer_symbol):
                        self.board[i][j] = " "
                        return i, j
                    self.board[i][j] = " "
        # Si no puede ganar, bloquea al jugador si es posible
        for i, j in empty_cells:
            self.board[i][j] = self.player_symbol
            if self.check_winner(self.player_symbol):
                self.board[i][j] = " "
                return i, j
            self.board[i][j] = " "
        # Si no puede bloquear al jugador, elige un movimiento aleatorio
        return random.choice(empty_cells)

    def check_winner(self, player):
        """
        Comprueba si hay un ganador.
        """
        for i in range(3):
            if all(self.board[i][j] == player for j in range(3)) or \
               all(self.board[j][i] == player for j in range(3)) or \
               all(self.board[i][i] == player for i in range(3)) or \
               all(self.board[i][2-i] == player for i in range(3)):
                return True
        return False

    def check_draw(self):
        """
        Comprueba si hay un empate.
        """
        return all(cell != " " for row in self.board for cell in row)

    def reset_board(self):
        """
        Reinicia el tablero.
        """
        self.board = [[" " for _ in range(3)] for _ in range(3)]
        for row in self.buttons:
            for button in row:
                button.config(text=" ", state="normal")

        self.player_label.config(text=f"Jugador: {self.player_wins}")
        self.computer_label.config(text=f"Consola: {self.computer_wins}")


if __name__ == "__main__":
    app = TicTacToe()
    app.mainloop()
