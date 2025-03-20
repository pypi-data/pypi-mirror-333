import socket
import sys

class GameConnexion:
    def __init__(self, host="127.0.0.1", console_port=58591, matrix_port=58600, player_count=1):
        self.host = host
        self.console_port = console_port
        self.matrix_port = matrix_port
        self.player_count = player_count

        self.client_socket = None
        self.matrix_socket = None

    def connect(self, game=None):
        """Établit les connexions à la console et à la matrice LED."""
        # Connexion à la console
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.host, self.console_port))
        self.client_socket.sendall(f"{game} démarré avec {self.player_count} joueur(s)".encode())

        # Connexion à la matrice LED
        self.matrix_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.matrix_socket.connect((self.host, self.matrix_port))

    def send_frame(self, frame=None):
        """Envoie une trame personnalisée à la matrice LED."""
        if frame is None:
            # Trame par défaut
            if self.player_count == 1:
                frame = ";".join(["(0,0,255)"] * 256)  # Tout en bleu
            else:
                frame = ";".join(["(255,0,0)"] * 128 + ["(0,0,255)"] * 128)  # Rouge et bleu

        self.matrix_socket.sendall(frame.encode())

    def listen_for_commands(self):
        """Boucle pour écouter les commandes de la console."""
        running = True
        while running:
            try:
                command = self.client_socket.recv(1024).decode()
                if not command:
                    break
                if command == "KILL":
                    running = False
            except ConnectionResetError:
                print("Connexion à la console perdue.")
                running = False

    def close(self):
        """Ferme les connexions proprement."""
        print("Fin du jeu 1.")
        if self.matrix_socket:
            self.matrix_socket.close()
        if self.client_socket:
            self.client_socket.close()
        sys.exit(0)
