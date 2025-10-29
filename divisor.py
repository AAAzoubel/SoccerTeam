import tkinter as tk                     # Importa a biblioteca Tkinter (interface gráfica)
from tkinter import messagebox, filedialog  # Importa caixas de mensagem e seletor de arquivos
import csv                               # Importa módulo para ler arquivos CSV
import random                            # Importa módulo para gerar aleatoriedade

# ---------------- Classe principal da aplicação ----------------
class SoccerTeamApp:
    def __init__(self, root):
        # Inicializa a janela principal
        self.root = root
        self.root.title("Soccer Team Divider")  # Define o título da janela
        self.players = []                       # Lista para armazenar jogadores do modo rápido
        self.imported_players_temp = []         # Lista temporária para armazenar jogadores importados do CSV
        self.main_menu()                        # Exibe o menu principal ao iniciar

    # ---------------- Tela inicial (menu principal) ----------------
    def main_menu(self):
        self.clear_frame()  # Limpa qualquer tela anterior
        tk.Label(self.root, text="Welcome to Soccer Team Divider!", font=("Helvetica", 16)).pack(pady=20)
        tk.Button(self.root, text="Quick Match", command=self.quick_match_menu, width=20).pack(pady=5)
        tk.Button(self.root, text="Create Tournament", command=self.tournament_menu, width=20).pack(pady=5)

    # ---------------- Menu do modo rápido ----------------
    def quick_match_menu(self):
        self.clear_frame()
        tk.Label(self.root, text="Choose Match Type:", font=("Helvetica", 14)).pack(pady=10)
        # Cada botão define o número de jogadores (7x7 = 14 jogadores, etc.)
        tk.Button(self.root, text="Society (7x7)", command=lambda: self.register_players(14)).pack(pady=5)
        tk.Button(self.root, text="Futsal (5x5)", command=lambda: self.register_players(10)).pack(pady=5)
        tk.Button(self.root, text="Normal Field (11x11)", command=lambda: self.register_players(22)).pack(pady=5)
        tk.Button(self.root, text="Back", command=self.main_menu).pack(pady=10)

    # ---------------- Cadastro manual ou importação de jogadores ----------------
    def register_players(self, num_players):
        self.clear_frame()
        self.num_players = num_players  # Guarda o número de jogadores necessários
        self.players = []               # Reinicia a lista de jogadores

        tk.Label(self.root, text=f"Register {num_players} players", font=("Helvetica", 14)).pack(pady=10)
        tk.Button(self.root, text="Import Players from CSV", command=lambda: self.import_players_from_csv("quick")).pack(pady=5)

        # Campos de entrada manual de jogador
        tk.Label(self.root, text="Enter Name:").pack(pady=2)
        self.name_entry = tk.Entry(self.root, width=30)
        self.name_entry.pack(pady=2)
        tk.Label(self.root, text="Enter Skill (1-10):").pack(pady=2)
        self.skill_entry = tk.Entry(self.root, width=30)
        self.skill_entry.pack(pady=2)

        # Botões para adicionar jogador ou finalizar
        tk.Button(self.root, text="Add Player", command=self.add_player).pack(pady=5)
        tk.Button(self.root, text="Finalize Teams", command=self.finalize_teams).pack(pady=5)
        tk.Button(self.root, text="Back", command=self.quick_match_menu).pack(pady=10)

    # ---------------- Adiciona jogador individual ----------------
    def add_player(self):
        name = self.name_entry.get().strip()   # Lê o nome
        try:
            skill = float(self.skill_entry.get().strip())  # Lê e converte a habilidade
            if not (1 <= skill <= 10):          # Valida faixa de 1 a 10
                raise ValueError("Skill must be between 1 and 10.")
            if len(self.players) < self.num_players:       # Verifica se ainda cabe jogador
                self.players.append({'name': name, 'overall_skill': skill})
                messagebox.showinfo("Player Added", f"{name} added with skill {skill}!")
                self.name_entry.delete(0, tk.END)          # Limpa os campos
                self.skill_entry.delete(0, tk.END)
            else:
                messagebox.showwarning("Limit Reached", "All players have been registered.")
        except ValueError as e:
            messagebox.showerror("Invalid Input", str(e))

    # ---------------- Divide os times ----------------
    def finalize_teams(self):
        if len(self.players) < self.num_players:
            messagebox.showwarning("Incomplete", f"Please add all {self.num_players} players.")
            return
        team_a, team_b = self.balance_teams()  # Cria os dois times balanceados
        self.show_teams(team_a, team_b)        # Mostra o resultado

    # ---------------- Lógica de balanceamento de times ----------------
    def balance_teams(self):
        # Ordena os jogadores por habilidade (melhor → pior)
        players_sorted = sorted(self.players, key=lambda x: x['overall_skill'], reverse=True)
        
        # Embaralha um pouco para evitar divisões sempre iguais
        random.shuffle(players_sorted)

        team_a, team_b = [], []

        # Divide os jogadores em pares e distribui alternadamente
        for i in range(0, len(players_sorted), 2):
            pair = players_sorted[i:i+2]
            random.shuffle(pair)  # muda a ordem dentro do par
            if (i // 2) % 2 == 0:
                team_a.extend(pair)
            else:
                team_b.extend(pair)

        # Se o número de jogadores for ímpar, coloca o último no time mais fraco
        if len(team_a) != len(team_b):
            average_team_A = sum(player['overall_skill'] for player in team_a) / len(team_a)
            average_team_B = sum(player['overall_skill'] for player in team_b) / len(team_b)
            extra_player = players_sorted[-1]
            if average_team_A > average_team_B:
                team_b.append(extra_player)
            else:
                team_a.append(extra_player)

        return team_a, team_b

    # ---------------- Mostra os times criados ----------------
    def show_teams(self, team_a, team_b):
        self.clear_frame()
        tk.Label(self.root, text="Teams Divided!", font=("Helvetica", 16)).pack(pady=10)
        tk.Label(self.root, text="Team A:", font=("Helvetica", 14)).pack(pady=5)
        for player in team_a:
            tk.Label(self.root, text=f"{player['name']} (Skill: {player['overall_skill']})").pack()
        tk.Label(self.root, text="Team B:", font=("Helvetica", 14)).pack(pady=5)
        for player in team_b:
            tk.Label(self.root, text=f"{player['name']} (Skill: {player['overall_skill']})").pack()
        tk.Button(self.root, text="Back to Main Menu", command=self.main_menu).pack(pady=10)

    # ---------------- Menu de torneio ----------------
    def tournament_menu(self):
        self.clear_frame()
        tk.Label(self.root, text="Tournament Setup", font=("Helvetica", 16)).pack(pady=10)

        # Define número de times e jogadores por time
        tk.Label(self.root, text="Number of Teams:").pack()
        self.team_count_entry = tk.Entry(self.root, width=10)
        self.team_count_entry.pack(pady=5)

        tk.Label(self.root, text="Players per Team:").pack()
        self.players_per_team_entry = tk.Entry(self.root, width=10)
        self.players_per_team_entry.pack(pady=5)

        tk.Button(self.root, text="Import Players from CSV", command=lambda: self.import_players_from_csv("tournament")).pack(pady=5)
        tk.Button(self.root, text="Next", command=self.start_tournament_registration).pack(pady=10)
        tk.Button(self.root, text="Back", command=self.main_menu).pack(pady=10)

    # ---------------- Início do registro do torneio ----------------
    def start_tournament_registration(self):
        try:
            # Lê número de times e jogadores por time
            num_teams = int(self.team_count_entry.get())
            players_per_team = int(self.players_per_team_entry.get())
            if num_teams <= 0 or players_per_team <= 0:
                raise ValueError

            total_players = num_teams * players_per_team
            # Guarda a configuração
            self.tournament_config = {"num_teams": num_teams, "players_per_team": players_per_team, "total_players": total_players}

            # Se houver jogadores importados do CSV, usa eles
            if self.imported_players_temp:
                self.tournament_players = self.imported_players_temp[:total_players]
                self.create_teams()
            else:
                self.register_tournament_players(total_players)
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers")

    # ---------------- Registro manual de jogadores do torneio ----------------
    def register_tournament_players(self, total_players):
        self.clear_frame()
        self.tournament_players = []
        self.total_players = total_players

        tk.Label(self.root, text=f"Register {total_players} players", font=("Helvetica", 14)).pack(pady=10)
        tk.Label(self.root, text="Enter Name:").pack()
        self.name_entry = tk.Entry(self.root, width=30)
        self.name_entry.pack(pady=5)
        tk.Label(self.root, text="Enter Skill (1-10):").pack()
        self.skill_entry = tk.Entry(self.root, width=30)
        self.skill_entry.pack(pady=5)
        tk.Button(self.root, text="Add Player", command=self.add_tournament_player).pack(pady=5)
        tk.Button(self.root, text="Create Teams", command=self.create_teams).pack(pady=5)
        tk.Button(self.root, text="Back", command=self.tournament_menu).pack(pady=10)

    def add_tournament_player(self):
        name = self.name_entry.get().strip()
        try:
            skill = float(self.skill_entry.get().strip())
            if not (1 <= skill <= 10):
                raise ValueError
            if len(self.tournament_players) < self.total_players:
                self.tournament_players.append({'name': name, 'overall_skill': skill})
                messagebox.showinfo("Player Added", f"{name} added!")
                self.name_entry.delete(0, tk.END)
                self.skill_entry.delete(0, tk.END)
            else:
                messagebox.showwarning("Limit Reached", "All players have been registered.")
        except ValueError:
            messagebox.showerror("Invalid Input", "Enter valid skill (1-10).")

    # ---------------- Importação universal de CSV ----------------
    def import_players_from_csv(self, mode):
        filepath = filedialog.askopenfilename(
            title="Select CSV file",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if not filepath:
            return

        try:
            with open(filepath, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                players = [
                    {'name': row['name'].strip(), 'overall_skill': float(row['skill'])}
                    for row in reader
                    if row.get('name') and row.get('skill') and 1 <= float(row['skill']) <= 10
                ]

            if not players:
                messagebox.showerror("Error", "No valid players found in file.")
                return

            if mode == "quick":
                # Modo rápido → já divide times direto
                self.players = players[:self.num_players]
                messagebox.showinfo("Import Success", f"Imported {len(self.players)} players!")
                self.finalize_teams()
            else:
                # Torneio → guarda pra usar depois
                self.imported_players_temp = players
                messagebox.showinfo("Import Success", f"Imported {len(players)} players! They’ll be used when you click Next.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to read file: {e}")

    # ---------------- Criação dos times do torneio ----------------
    def create_teams(self):
        if len(self.tournament_players) < self.tournament_config["total_players"]:
            messagebox.showwarning("Incomplete", "Not all players registered.")
            return

        # Ordena por habilidade e distribui de forma equilibrada
        sorted_players = sorted(self.tournament_players, key=lambda x: x['overall_skill'], reverse=True)
        teams = [[] for _ in range(self.tournament_config["num_teams"])]
        for i, p in enumerate(sorted_players):
            teams[i % self.tournament_config["num_teams"]].append(p)

        # Mostra os times
        self.show_tournament_teams(teams)

    # ---------------- Exibição dos times antes do torneio ----------------
    def show_tournament_teams(self, teams):
        self.clear_frame()
        tk.Label(self.root, text="Tournament Teams Divided!", font=("Helvetica", 16)).pack(pady=10)
        for idx, team in enumerate(teams, start=1):
            tk.Label(self.root, text=f"Team {idx}:", font=("Helvetica", 14)).pack(pady=5)
            for player in team:
                tk.Label(self.root, text=f"{player['name']} (Skill: {player['overall_skill']:.1f})").pack()

        # Botão para iniciar o mata-mata
        tk.Button(self.root, text="Start Tournament", command=lambda: self.start_knockout(
            [{"name": f'Team {i+1}', "players": team} for i, team in enumerate(teams)]
        )).pack(pady=10)

    # ---------------- Início do torneio mata-mata ----------------
    def start_knockout(self, teams):
        random.shuffle(teams)  # Embaralha a ordem dos times para chaveamento aleatório
        self.current_round = 1
        self.current_teams = teams
        self.show_tournament_round()

    # ---------------- Exibe as rodadas ----------------
    def show_tournament_round(self):
        self.clear_frame()

        # Se sobrou só 1 time → campeão
        if len(self.current_teams) == 1:
            champion = self.current_teams[0]
            tk.Label(self.root, text=f"🏆 Champion: {champion['name']} 🏆", font=("Helvetica", 18)).pack(pady=20)
            for player in champion["players"]:
                tk.Label(self.root, text=f"{player['name']} (Skill: {player['overall_skill']})").pack()
            tk.Button(self.root, text="Back to Main Menu", command=self.main_menu).pack(pady=20)
            return

        tk.Label(self.root, text=f"Round {self.current_round} - {len(self.current_teams)} Teams", font=("Helvetica", 16)).pack(pady=10)
        self.round_matches = []

        # Cria pares de confrontos
        for i in range(0, len(self.current_teams), 2):
            if i + 1 < len(self.current_teams):
                self.round_matches.append((self.current_teams[i], self.current_teams[i+1]))

        self.next_round_winners = []

        def create_win_button(parent, team):
            # Botão que registra o vencedor
            return tk.Button(parent, text=f"{team['name']} Wins", command=lambda t=team: self.register_winner(t))

        # Mostra cada confronto com os dois times
        for match_number, (team1, team2) in enumerate(self.round_matches, start=1):
            frame = tk.Frame(self.root, borderwidth=2, relief="groove", padx=10, pady=10)
            frame.pack(pady=8)

            tk.Label(frame, text=f"Match {match_number}: {team1['name']} vs {team2['name']}", font=("Helvetica", 12, "bold")).pack(pady=5)

            # Botões para registrar quem venceu
            create_win_button(frame, team1).pack(side="left", padx=10, pady=5)
            create_win_button(frame, team2).pack(side="right", padx=10, pady=5)

    # ---------------- Registra o vencedor e avança para a próxima rodada ----------------
    def register_winner(self, team):
        self.next_round_winners.append(team)
        # Quando todos os confrontos da rodada tiverem vencedores, passa pra próxima
        if len(self.next_round_winners) == len(self.round_matches):
            self.current_teams = self.next_round_winners
            self.current_round += 1
            self.show_tournament_round()

    # ---------------- Limpa a tela ----------------
    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()

# ---------------- Executa o app ----------------
root = tk.Tk()
app = SoccerTeamApp(root)
root.mainloop()
