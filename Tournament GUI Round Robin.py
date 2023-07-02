import tkinter as tk
from tkinter import ttk

class MainScreen:
    def __init__(self, master):
        self.master = master
        self.master.title("Fencing Tournament")
        self.master.geometry("800x600")

        self.style = ttk.Style()
        self.style.configure("TButton",
                             font=('Helvetica', 16),
                             padding=10)

        self.fencer_list = []
        self.tournament = None

        self.create_widgets()

    def create_widgets(self):
        self.add_fencers_button = ttk.Button(self.master, text="Add Fencers", command=self.open_add_fencer, style="TButton")
        self.add_fencers_button.pack(padx=40, pady=20)

        self.edit_fencers_button = ttk.Button(self.master, text="Edit Fencers", command=self.open_edit_fencers, style="TButton")
        self.edit_fencers_button.pack(padx=40, pady=20)

        self.setup_tournament_button = ttk.Button(self.master, text="Setup Tournament", command=self.open_setup_tournament, style="TButton")
        self.setup_tournament_button.pack(padx=40, pady=20)

        self.start_tournament_button = ttk.Button(self.master, text="Start Tournament", command=self.start_tournament, style="TButton")
        self.start_tournament_button.pack(padx=40, pady=20)

    def open_add_fencer(self):
        new_window = tk.Toplevel(self.master)
        AddFencersScreen(new_window, self.fencer_list)

    def open_edit_fencers(self):
        new_window = tk.Toplevel(self.master)
        EditFencersScreen(new_window, self.fencer_list)

    def open_setup_tournament(self):
        new_window = tk.Toplevel(self.master)
        SetupTournamentScreen(new_window)

    def start_tournament(self):
        new_window = tk.Toplevel(self.master)
        setup_tournament_screen = SetupTournamentScreen(new_window)
        num_pits = int(setup_tournament_screen.get_pits_value())
        matches_per_fencer = int(setup_tournament_screen.get_matches_value())
        bracket_levels = int(setup_tournament_screen.get_bracket_value())
        TournamentScreen(new_window, self.fencer_list, num_pits, matches_per_fencer, bracket_levels)


class EditFencersScreen:
    def __init__(self, master, fencer_list):
        self.master = master
        self.master.title("Edit Fencers")
        self.master.geometry("800x600")

        self.style = ttk.Style()
        self.style.configure("TButton", font=('Helvetica', 16), padding=10)
        self.style.configure("TLabel", font=('Helvetica', 16), padding=10)
        self.style.configure("TEntry", font=('Helvetica', 16), padding=10)
        
        self.fencer_list = fencer_list
        self.selected_fencer = tk.StringVar(self.master)
        self.create_widgets()

    def create_widgets(self):
        self.fencer_menu = ttk.Combobox(self.master, textvariable=self.selected_fencer, 
                                        values=[fencer.name for fencer in self.fencer_list], font=('Helvetica', 16))
        self.fencer_menu.grid(row=0, column=0, padx=20, pady=20)

        self.name_label = ttk.Label(self.master, text="Name:", style="TLabel")
        self.name_label.grid(row=1, column=0, padx=20, pady=20)

        self.name_entry = ttk.Entry(self.master, style="TEntry")
        self.name_entry.grid(row=1, column=1, padx=20, pady=20)

        self.club_label = ttk.Label(self.master, text="Club:", style="TLabel")
        self.club_label.grid(row=2, column=0, padx=20, pady=20)

        self.club_entry = ttk.Entry(self.master, style="TEntry")
        self.club_entry.grid(row=2, column=1, padx=20, pady=20)

        self.update_button = ttk.Button(self.master, text="Update Fencer", command=self.update_fencer, style="TButton")
        self.update_button.grid(row=3, column=0, columnspan=2, padx=20, pady=20)

        self.delete_button = ttk.Button(self.master, text="Delete Fencer", command=self.delete_fencer, style="TButton")
        self.delete_button.grid(row=4, column=0, columnspan=2, padx=20, pady=20)

    def update_fencer(self):
        selected_name = self.selected_fencer.get()
        new_name = self.name_entry.get()
        new_club = self.club_entry.get()

        for fencer in self.fencer_list:
            if fencer.name == selected_name:
                fencer.name = new_name
                fencer.club = new_club
                break

    def delete_fencer(self):
        selected_name = self.selected_fencer.get()

        for i, fencer in enumerate(self.fencer_list):
            if fencer.name == selected_name:
                del self.fencer_list[i]

    def update_fencer(self):
        selected_name = self.selected_fencer.get().strip()
        new_name = self.name_entry.get().strip()
        new_club = self.club_entry.get().strip()

        if selected_name and new_name and new_club:
            for fencer in self.fencer_list:
                if fencer.name == selected_name:
                    fencer.name = new_name
                    fencer.club = new_club
                    self.fencer_menu['values'] = [fencer.name for fencer in self.fencer_list]
                    break
        else:
            print("All fields must be filled out.")
            
    def delete_fencer(self):
        selected_name = self.selected_fencer.get().strip()

        if selected_name:
            for i, fencer in enumerate(self.fencer_list):
                if fencer.name == selected_name:
                    del self.fencer_list[i]
                    self.fencer_menu['values'] = [fencer.name for fencer in self.fencer_list]
                    break
        else:
            print("No fencer selected.")

class AddFencersScreen:
    def __init__(self, master, fencer_list):
        self.master = master
        self.master.title("Add Fencers")
        self.master.geometry("600x500")

        self.style = ttk.Style()
        self.style.configure("TButton",
                             font=('Helvetica', 16),
                             padding=10)
        self.style.configure("TLabel",
                             font=('Helvetica', 16),
                             padding=10)
        self.style.configure("TEntry",
                             font=('Helvetica', 16),
                             padding=10)

        self.fencer_list = fencer_list

        self.club_options = ["Club 1", "Club 2", "Club 3", "Club 4", "Club 5"]

        self.create_widgets()
        self.master.bind('<Return>', self.add_fencer)

    def create_widgets(self):
        self.name_label = ttk.Label(self.master, text="Name:", style="TLabel")
        self.name_label.grid(row=0, column=0, padx=20, pady=20)

        self.name_entry = ttk.Entry(self.master, style="TEntry")
        self.name_entry.grid(row=0, column=1, padx=20, pady=20)

        self.club_label = ttk.Label(self.master, text="Club:", style="TLabel")
        self.club_label.grid(row=1, column=0, padx=20, pady=20)

        self.club_var = tk.StringVar(self.master)
        self.club_combo = ttk.Combobox(self.master, textvariable=self.club_var, values=self.club_options, font=('Helvetica', 16))
        self.club_combo.grid(row=1, column=1, padx=20, pady=20)

        self.add_fencer_button = ttk.Button(self.master, text="Add Fencer", command=self.add_fencer, style="TButton")
        self.add_fencer_button.grid(row=2, column=0, columnspan=2, padx=20, pady=20)

        self.done_button = ttk.Button(self.master, text="Done Adding Fencers", command=self.master.destroy, style="TButton")
        self.done_button.grid(row=3, column=0, columnspan=2, padx=20, pady=20)

    def add_fencer(self, event=None):
        new_fencer = Fencer(self.name_entry.get(), self.club_var.get())
        self.fencer_list.append(new_fencer)
        self.name_entry.delete(0, 'end')
    def add_fencer(self, event=None):
            fencer_name = self.name_entry.get().strip()
            fencer_club = self.club_var.get().strip()
        
            if fencer_name and fencer_club:
                new_fencer = Fencer(fencer_name, fencer_club)
                self.fencer_list.append(new_fencer)
                self.name_entry.delete(0, 'end')
            else:
                # Display a message box or some other notification to the user
                # about the missing information
                print("Both name and club must be filled out.")

class SetupTournamentScreen:
    def __init__(self, master):
        self.master = master
        self.master.title("Setup Tournament")
        self.master.geometry("600x500")

        self.style = ttk.Style()
        self.style.configure("TButton", font=('Helvetica', 16), padding=10)
        self.style.configure("TLabel", font=('Helvetica', 16), padding=10)
        self.style.configure("TEntry", font=('Helvetica', 16), padding=10)

        self.pits_value = tk.StringVar(value="2")  # Default value for number of pits
        self.matches_value = tk.StringVar(value="5")  # Default value for matches per fencer
        self.bracket_value = tk.StringVar(value="3")  # Default value for elimination bracket levels

        self.create_widgets()

    def create_widgets(self):
        self.pits_label = ttk.Label(self.master, text="Number of Pits:", style="TLabel")
        self.pits_label.grid(row=0, column=0, padx=20, pady=20)

        self.pits_entry = ttk.Entry(self.master, style="TEntry", textvariable=self.pits_value)
        self.pits_entry.grid(row=0, column=1, padx=20, pady=20)

        self.matches_label = ttk.Label(self.master, text="Matches per Fencer:", style="TLabel")
        self.matches_label.grid(row=1, column=0, padx=20, pady=20)

        self.matches_entry = ttk.Entry(self.master, style="TEntry", textvariable=self.matches_value)
        self.matches_entry.grid(row=1, column=1, padx=20, pady=20)

        self.bracket_label = ttk.Label(self.master, text="Elimination Bracket Levels:", style="TLabel")
        self.bracket_label.grid(row=2, column=0, padx=20, pady=20)

        self.bracket_entry = ttk.Entry(self.master, style="TEntry", textvariable=self.bracket_value)
        self.bracket_entry.grid(row=2, column=1, padx=20, pady=20)

        self.setup_button = ttk.Button(self.master, text="Setup Tournament", command=self.setup_tournament, style="TButton")
        self.setup_button.grid(row=3, column=0, columnspan=2, padx=20, pady=20)

    def setup_tournament(self):
        num_pits = int(self.pits_value.get())
        matches_per_fencer = int(self.matches_value.get())
        bracket_levels = int(self.bracket_value.get())

        # Validate the entries here and if everything is okay, setup the tournament
        # Update the tournament setup details in the application

    def get_pits_value(self):
        return self.pits_value.get()

    def get_matches_value(self):
        return self.matches_value.get()

    def get_bracket_value(self):
        return self.bracket_value.get()

class TournamentScreen:
    def __init__(self, master, fencer_list, num_pits, matches_per_fencer, bracket_levels):
        self.master = master
        self.fencer_list = fencer_list
        self.num_pits = num_pits
        self.matches_per_fencer = matches_per_fencer
        self.bracket_levels = bracket_levels

        self.pits = [[] for _ in range(num_pits)]
        self.available_fencers = self.fencer_list.copy()
        self.completed_matches = []

        self.create_widgets()
        self.update_screen()

    def create_widgets(self):
        self.pit_frames = []
        for i in range(self.num_pits):
            frame = ttk.Frame(self.master)
            frame.grid(row=i, column=0, padx=10, pady=10)

            fencer1_label = ttk.Label(frame, text="Fencer 1:")
            fencer1_label.grid(row=0, column=0)

            self.fencer1_entry = ttk.Entry(frame)
            self.fencer1_entry.grid(row=0, column=1)

            fencer1_score_label = ttk.Label(frame, text="Fencer 1 Score:")
            fencer1_score_label.grid(row=1, column=0)

            self.fencer1_score_entry = ttk.Entry(frame)
            self.fencer1_score_entry.grid(row=1, column=1)

            fencer2_label = ttk.Label(frame, text="Fencer 2:")
            fencer2_label.grid(row=2, column=0)

            self.fencer2_entry = ttk.Entry(frame)
            self.fencer2_entry.grid(row=2, column=1)

            fencer2_score_label = ttk.Label(frame, text="Fencer 2 Score:")
            fencer2_score_label.grid(row=3, column=0)

            self.fencer2_score_entry = ttk.Entry(frame)
            self.fencer2_score_entry.grid(row=3, column=1)

            score_submit_button = ttk.Button(frame, text="Submit Scores", command=lambda pit_index=i: self.complete_match(pit_index))
            score_submit_button.grid(row=4, column=0, columnspan=2)

            self.pit_frames.append(frame)

    def update_screen(self):
        # This function should update the screen whenever a match is completed
        # or a new match needs to be set up.
        # It might involve refreshing the displayed matches, fencer statistics, etc.
        pass

    def pair_fencers(self, fencers):
        fencers = self.calculate_and_sort_elo(fencers)

        # First try to match fencers using ELO
        for i, fencer1 in enumerate(fencers):
            for j in range(i + 1, len(fencers)):
                fencer2 = fencers[j]
                if fencer2 not in fencer1.previous_opponents and fencer1.club != fencer2.club:
                    return fencer1, fencer2

        # If that fails, try Swiss pairing
        fencers.sort(key=lambda fencer: fencer.points, reverse=True)
        for i, fencer1 in enumerate(fencers):
            for j in range(i + 1, len(fencers)):
                fencer2 = fencers[j]
                if fencer2 not in fencer1.previous_opponents and fencer1.club != fencer2.club:
                    return fencer1, fencer2

        # If all else fails, try to find the least bad pairing
        least_elo_difference = float('inf')
        best_pair = None
        for fencer1, fencer2 in itertools.combinations(fencers, 2):
            if fencer2 not in fencer1.previous_opponents and fencer1.club != fencer2.club:
                elo_difference = abs(fencer1.elo - fencer2.elo)
                if elo_difference < least_elo_difference:
                    least_elo_difference = elo_difference
                    best_pair = (fencer1, fencer2)

        return best_pair if best_pair else (None, None)

    def complete_match(self, pit_index):
        frame = self.pit_frames[pit_index]
        
        fencer1_name = self.fencer1_entry.get()
        fencer1_score = float(self.fencer1_score_entry.get())

        fencer2_name = self.fencer2_entry.get()
        fencer2_score = float(self.fencer2_score_entry.get())

        for fencer in self.fencer_list:
            if fencer.name == fencer1_name:
                fencer.update_points(fencer1_score)
                # Update other fencer statistics as needed
            elif fencer.name == fencer2_name:
                fencer.update_points(fencer2_score)
                # Update other fencer statistics as needed

        self.completed_matches.append((fencer1_name, fencer2_name))
        self.pits[pit_index] = []
        
        # If there are still available fencers, start a new match
        if len(self.available_fencers) >= 2:
            fencer1, fencer2 = self.pair_fencers(self.available_fencers)
            self.pits[pit_index] = [fencer1, fencer2]
            self.available_fencers.remove(fencer1)
            self.available_fencers.remove(fencer2)

            # Update the entry fields with the new match
            self.fencer1_entry.delete(0, tk.END)
            self.fencer1_entry.insert(0, fencer1.name)
            self.fencer2_entry.delete(0, tk.END)
            self.fencer2_entry.insert(0, fencer2.name)

class Fencer:
    def __init__(self, name, club, elo=1500):
        self.name = name
        self.club = club
        self.elo = elo
        self.points = 0
        self.paired = False
        self.previous_opponents = []
        self.performance = []
        self.k_factor = 40 

    def update_elo(self, opponent_elo, score, opponent_score):
        expected_score = 1 / (1 + 10 ** ((opponent_elo - self.elo) / 400))
        actual_score = score / (score + opponent_score)
        elo_change = self.k_factor * (actual_score - expected_score)
        self.elo += elo_change

        # Update the K-factor based on point differential
        self.k_factor *= (1 + abs(score - opponent_score) / (score + opponent_score))

    def update_points(self, points):
        self.points += points

    def update_performance(self, opponent_name, score, opponent_score):
        self.performance.append({
            "Opponent": opponent_name,
            "Score": score,
            "Opponent Score": opponent_score
        })

    def recalculate_elo(self, fencers):
        # Reset the ELO and K-factor
        self.elo = 1500
        self.k_factor = 40

        # Re-run the ELO calculations based on the updated ELOs of the opponents
        for performance in self.performance:
            opponent_elo = next((opp.elo for opp in fencers if opp.name == performance["Opponent"]), 1500)
            self.update_elo(opponent_elo, performance["Score"], performance["Opponent Score"])






root = tk.Tk()
app = MainScreen(root)
root.mainloop()