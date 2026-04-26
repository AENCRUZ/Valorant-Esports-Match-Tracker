import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

# --- 1. Database Configuration and Connection ---
# IMPORTANT: Replace these with your actual database credentials
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": None,  # <-- !!! CHANGE THIS TO YOUR MYSQL PASSWORD !!!
    "database": "ValorantEsportsTracker" 
}

def connect_db():
    """Establishes a connection to the MySQL database."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except mysql.connector.Error as err:
        messagebox.showerror("DB Error", f"Failed to connect to MySQL: {err}")
        return None

# --- Helper Functions for Foreign Key Dropdowns ---

def get_team_ids_names(conn):
    """Fetches Team IDs and Names for use in dropdowns."""
    if not conn: return []
    cursor = conn.cursor()
    query = "SELECT Team_ID, Team_Name FROM TEAM ORDER BY Team_Name"
    try:
        cursor.execute(query)
        # Returns a list of strings: ["ID - Name", ...]
        return [f"{row[0]} - {row[1]}" for row in cursor.fetchall()]
    except mysql.connector.Error as err:
        print(f"Error fetching teams: {err}")
        return []
    finally:
        cursor.close()

def get_tournament_ids_names(conn):
    """Fetches Tournament IDs and Names for use in dropdowns."""
    if not conn: return []
    cursor = conn.cursor()
    query = "SELECT Tourn_ID, Tourn_Name FROM TOURNAMENT ORDER BY Tourn_Name"
    try:
        cursor.execute(query)
        # Returns a list of strings: ["ID - Name", ...]
        return [f"{row[0]} - {row[1]}" for row in cursor.fetchall()]
    except mysql.connector.Error as err:
        print(f"Error fetching tournaments: {err}")
        return []
    finally:
        cursor.close()

# --- 2. TEAM Management Window (CRUD) ---

class TeamManager(tk.Toplevel):
    """
    Implements a full CRUD interface for the TEAM table.
    """
    def __init__(self, master):
        super().__init__(master)
        self.title("Manage Teams")
        self.geometry("800x600")
        self.db_conn = connect_db()
        self.create_widgets()
        self.load_data()

    def create_widgets(self):
        """Sets up the layout, input fields, and display area."""
        
        # --- 2.1 Input Frame (Top) ---
        input_frame = ttk.LabelFrame(self, text="Team Data Input", padding="10")
        input_frame.pack(padx=10, pady=10, fill="x")

        # Fields: Team_ID (PK), Team_Name, Coach_Name
        tk.Label(input_frame, text="Team ID (e.g., SEN):").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.team_id_entry = tk.Entry(input_frame, width=10)
        self.team_id_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        tk.Label(input_frame, text="Team Name:").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.name_entry = tk.Entry(input_frame, width=30)
        self.name_entry.grid(row=0, column=3, padx=5, pady=5, sticky="w")

        tk.Label(input_frame, text="Coach Name:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.coach_entry = tk.Entry(input_frame, width=30)
        self.coach_entry.grid(row=1, column=1, columnspan=2, padx=5, pady=5, sticky="w")

        # --- 2.2 CRUD Buttons ---
        button_frame = ttk.Frame(self)
        button_frame.pack(padx=10, pady=5)

        ttk.Button(button_frame, text="Add Team (Create)", command=self.add_team).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Update Selected (Update)", command=self.update_team).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Delete Selected (Delete)", command=self.delete_team).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Clear Form", command=self.clear_form).pack(side=tk.LEFT, padx=5)

        # --- 2.3 Data Display Area (Bottom) ---
        columns = ("Team ID", "Team Name", "Coach Name")
        self.tree = ttk.Treeview(self, columns=columns, show="headings")
        self.tree.pack(padx=10, pady=10, fill="both", expand=True)

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center")

        self.tree.bind('<<TreeviewSelect>>', self.select_item)

    def clear_form(self):
        """Clears all input fields."""
        self.team_id_entry.delete(0, tk.END)
        self.name_entry.delete(0, tk.END)
        self.coach_entry.delete(0, tk.END)
        self.team_id_entry.config(state='normal')

    def select_item(self, event):
        """When a row is selected, populate the form for potential update/delete."""
        selected_item = self.tree.focus()
        if not selected_item:
            return

        values = self.tree.item(selected_item, 'values')
        self.clear_form()

        # Populate form
        self.team_id_entry.insert(0, values[0])
        self.name_entry.insert(0, values[1])
        self.coach_entry.insert(0, values[2])
        
        # Prevent editing the Primary Key during an update operation
        self.team_id_entry.config(state='disabled') 

    # --- 2.4 CRUD Implementations ---

    def load_data(self):
        """R (Read) - Retrieves all records and displays them in the Treeview."""
        for item in self.tree.get_children():
            self.tree.delete(item) 
            
        if not self.db_conn: return

        cursor = self.db_conn.cursor()
        query = "SELECT Team_ID, Team_Name, Coach_Name FROM TEAM"
        try:
            cursor.execute(query)
            for row in cursor.fetchall():
                self.tree.insert('', tk.END, values=row)
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Failed to load data: {err}")
        finally:
            cursor.close()

    def add_team(self):
        """C (Create) - Inserts a new team record."""
        team_id = self.team_id_entry.get().upper()
        name = self.name_entry.get()
        coach = self.coach_entry.get()

        if not team_id or not name:
            messagebox.showwarning("Input Error", "Team ID and Team Name are required.")
            return

        if not self.db_conn: return
        cursor = self.db_conn.cursor()
        
        # The SQL INSERT statement
        sql = "INSERT INTO team (Team_ID, Team_Name, Coach_Name) VALUES (%s, %s, %s)"
        try:
            cursor.execute(sql, (team_id, name, coach))
            self.db_conn.commit()
            messagebox.showinfo("Success", f"Team {name} added successfully.")
            self.clear_form()
            self.load_data() 
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Failed to add team: {err}")
        finally:
            cursor.close()

    def update_team(self):
        """U (Update) - Updates the selected team's details."""
        selected_item = self.tree.focus()
        if not selected_item:
            messagebox.showwarning("Selection Error", "Please select a team to update.")
            return

        team_id_pk = self.tree.item(selected_item, 'values')[0]
        new_name = self.name_entry.get()
        new_coach = self.coach_entry.get()
        
        if not self.db_conn: return
        cursor = self.db_conn.cursor()

        # The SQL UPDATE statement
        sql = "UPDATE team SET Team_Name = %s, Coach_Name = %s WHERE Team_ID = %s"
        try:
            cursor.execute(sql, (new_name, new_coach, team_id_pk))
            self.db_conn.commit()
            messagebox.showinfo("Success", f"Team {new_name} updated successfully.")
            self.clear_form()
            self.load_data() 
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Failed to update team: {err}")
        finally:
            cursor.close()

    def delete_team(self):
        """D (Delete) - Deletes the selected team record."""
        selected_item = self.tree.focus()
        if not selected_item:
            messagebox.showwarning("Selection Error", "Please select a team to delete.")
            return

        team_id = self.tree.item(selected_item, 'values')[0]
        name = self.tree.item(selected_item, 'values')[1]

        if not messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete Team {name}?"):
            return

        if not self.db_conn: return
        cursor = self.db_conn.cursor()
        
        # The SQL DELETE statement
        sql = "DELETE FROM team WHERE Team_ID = %s"
        try:
            cursor.execute(sql, (team_id,))
            self.db_conn.commit()
            messagebox.showinfo("Success", f"Team {name} deleted successfully.")
            self.clear_form()
            self.load_data() 
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", 
                                 f"Failed to delete team (Check Foreign Key constraints): {err}")
        finally:
            cursor.close()

# --- MANAGE PLAYER window ---

class PlayerManager(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)

        # Window settings
        self.title("Player Manager")
        self.geometry("700x500")
        self.configure(bg="#0f1923")

        # Variables
        self.player_id_var = tk.StringVar()
        self.ign_var = tk.StringVar()
        self.realname_var = tk.StringVar()
        self.team_var = tk.StringVar()

        # Title
        tk.Label(
            self, text="Player Manager",
            font=("Helvetica", 18, "bold"),
            bg="#0f1923", fg="white"
        ).pack(pady=10)

        # Form
        form = tk.Frame(self, bg="#0f1923")
        form.pack(pady=10)

        fields = [
            ("Player ID:", self.player_id_var),
            ("IGN:", self.ign_var),
            ("Real Name:", self.realname_var),
        ]

        for i, (label, var) in enumerate(fields):
            tk.Label(form, text=label, fg="white", bg="#0f1923",
                     font=("Helvetica", 12)).grid(row=i, column=0, padx=10, pady=5, sticky="w")
            tk.Entry(form, textvariable=var, width=30).grid(row=i, column=1, pady=5)

        # Team dropdown
        tk.Label(form, text="Team:", fg="white", bg="#0f1923",
                 font=("Helvetica", 12)).grid(row=3, column=0, padx=10, pady=5, sticky="w")

        self.team_combo = ttk.Combobox(
            form, textvariable=self.team_var, width=27, state="readonly"
        )
        self.team_combo.grid(row=3, column=1, pady=5)

        # Buttons
        btn_frame = tk.Frame(self, bg="#0f1923")
        btn_frame.pack(pady=10)

        buttons = [
            ("Add Player", self.add_player),
            ("Update Player", self.update_player),
            ("Delete Player", self.delete_player),
            ("Clear", self.clear_fields),
        ]

        for txt, cmd in buttons:
            tk.Button(btn_frame, text=txt, command=cmd,
                      bg="#ff4655", fg="white", width=12).pack(side="left", padx=5)

        # Table
        table_frame = tk.Frame(self, bg="#0f1923")
        table_frame.pack(fill="both", expand=True, pady=10)

        columns = ("Player_ID", "IGN", "Real_Name", "Team")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)

        self.tree.pack(fill="both", expand=True)
        self.tree.bind("<ButtonRelease-1>", self.select_player)

        # Load DB Data
        self.load_teams()
        self.load_players()

    # ---------------- DATABASE ---------------- #

    def load_teams(self):
        db = connect_db()
        if not db:
            return

        cursor = db.cursor()
        cursor.execute("SELECT Team_ID, Team_Name FROM TEAM")
        teams = cursor.fetchall()
        db.close()

        self.team_combo["values"] = ["None"] + [f"{tid} - {name}" for tid, name in teams]

    def get_team_id(self, value):
        if value == "None" or value == "":
            return None
        return value.split(" - ")[0]

    def load_players(self):
        db = connect_db()
        if not db:
            return

        cursor = db.cursor()
        cursor.execute("""
            SELECT P.Player_ID, P.IGN, P.Real_Name,
                   COALESCE(T.Team_Name, 'None')
            FROM PLAYER P
            LEFT JOIN TEAM T ON P.Team_ID = T.Team_ID
        """)
        rows = cursor.fetchall()
        db.close()

        self.tree.delete(*self.tree.get_children())
        for row in rows:
            self.tree.insert("", "end", values=row)

    # ---------------- CRUD ---------------- #

    def add_player(self):
        pid = self.player_id_var.get()
        ign = self.ign_var.get()
        real = self.realname_var.get()
        team = self.get_team_id(self.team_var.get())

        if pid == "" or ign == "" or real == "":
            messagebox.showerror("Error", "Player ID, IGN, and Real Name are required.")
            return

        db = connect_db()
        cursor = db.cursor()
        cursor.execute("""
            INSERT INTO PLAYER (Player_ID, IGN, Real_Name, Team_ID)
            VALUES (%s, %s, %s, %s)
        """, (pid, ign, real, team))
        db.commit()
        db.close()

        self.load_players()
        self.clear_fields()
        messagebox.showinfo("Success", "Player added!")

    def update_player(self):
        pid = self.player_id_var.get()
        if pid == "":
            messagebox.showerror("Error", "Select a player first.")
            return

        ign = self.ign_var.get()
        real = self.realname_var.get()
        team = self.get_team_id(self.team_var.get())

        db = connect_db()
        cursor = db.cursor()
        cursor.execute("""
            UPDATE PLAYER
            SET IGN=%s, Real_Name=%s, Team_ID=%s
            WHERE Player_ID=%s
        """, (ign, real, team, pid))
        db.commit()
        db.close()

        self.load_players()
        self.clear_fields()
        messagebox.showinfo("Success", "Player updated!")

    def delete_player(self):
        pid = self.player_id_var.get()
        if pid == "":
            messagebox.showerror("Error", "Select a player first.")
            return

        if not messagebox.askyesno("Confirm", "Delete this player?"):
            return

        db = connect_db()
        cursor = db.cursor()
        cursor.execute("DELETE FROM PLAYER WHERE Player_ID=%s", (pid,))
        db.commit()
        db.close()

        self.load_players()
        self.clear_fields()
        messagebox.showinfo("Success", "Player deleted!")

    # ---------------- UI ---------------- #

    def clear_fields(self):
        self.player_id_var.set("")
        self.ign_var.set("")
        self.realname_var.set("")
        self.team_var.set("None")

    def select_player(self, event):
        row = self.tree.focus()
        if not row:
            return

        data = self.tree.item(row)["values"]

        self.player_id_var.set(data[0])
        self.ign_var.set(data[1])
        self.realname_var.set(data[2])

        # Set team dropdown
        team_name = data[3]
        for val in self.team_combo["values"]:
            if val.endswith(f"- {team_name}"):
                self.team_var.set(val)
                return

        self.team_var.set("None")

# --- MANAGE TOURNAMENTS Window ---

class TournamentManager(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)

        # Window setup
        self.title("Manage Tournaments")
        self.geometry("800x600")
        self.configure(bg="#0f1923")

        # Variables
        self.tourn_id_var = tk.StringVar()
        self.tourn_name_var = tk.StringVar()
        self.start_date_var = tk.StringVar()
        self.prize_var = tk.StringVar()

        # Title Label
        tk.Label(
            self,
            text="Tournament Manager",
            font=("Helvetica", 18, "bold"),
            bg="#0f1923",
            fg="white"
        ).pack(pady=10)

        # Form Frame
        form = tk.Frame(self, bg="#0f1923")
        form.pack(pady=10)

        fields = [
            ("Tournament ID:", self.tourn_id_var),
            ("Tournament Name:", self.tourn_name_var),
            ("Start Date (YYYY-MM-DD):", self.start_date_var),
            ("Prize Pool:", self.prize_var)
        ]

        for i, (label, var) in enumerate(fields):
            tk.Label(form, text=label, fg="white", bg="#0f1923",
                     font=("Helvetica", 12)).grid(row=i, column=0, padx=10, pady=5, sticky="w")
            tk.Entry(form, textvariable=var, width=30).grid(row=i, column=1, pady=5)

        # Buttons Frame
        btn_frame = tk.Frame(self, bg="#0f1923")
        btn_frame.pack(pady=10)

        buttons = [
            ("Add", self.add_tournament),
            ("Update", self.update_tournament),
            ("Delete", self.delete_tournament),
            ("Clear", self.clear_fields)
        ]

        for txt, cmd in buttons:
            tk.Button(
                btn_frame, text=txt, command=cmd, bg="#ff4655",
                fg="white", width=12
            ).pack(side="left", padx=6)

        # Table Frame
        table_frame = tk.Frame(self, bg="#0f1923")
        table_frame.pack(fill="both", expand=True, pady=10)

        columns = ("Tourn_ID", "Tourn_Name", "Start_Date", "Prize_Pool")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=160)

        self.tree.pack(fill="both", expand=True)
        self.tree.bind("<ButtonRelease-1>", self.select_tournament)

        # Load data
        self.load_tournaments()

    # ---------------- DATABASE ---------------- #

    def load_tournaments(self):
        db = connect_db()
        if not db:
            return

        cursor = db.cursor()
        cursor.execute("SELECT Tourn_ID, Tourn_Name, Start_Date, Prize_Pool FROM TOURNAMENT")
        rows = cursor.fetchall()
        db.close()

        self.tree.delete(*self.tree.get_children())

        for row in rows:
            self.tree.insert("", "end", values=row)

    # ---------------- CRUD ---------------- #

    def add_tournament(self):
        tid = self.tourn_id_var.get()
        name = self.tourn_name_var.get()
        date = self.start_date_var.get()
        prize = self.prize_var.get()

        if tid == "" or name == "" or date == "" or prize == "":
            messagebox.showerror("Error", "All fields are required.")
            return

        db = connect_db()
        cursor = db.cursor()
        cursor.execute("""
            INSERT INTO TOURNAMENT (Tourn_ID, Tourn_Name, Start_Date, Prize_Pool)
            VALUES (%s, %s, %s, %s)
        """, (tid, name, date, prize))
        db.commit()
        db.close()

        self.load_tournaments()
        self.clear_fields()
        messagebox.showinfo("Success", "Tournament added!")

    def update_tournament(self):
        tid = self.tourn_id_var.get()
        if tid == "":
            messagebox.showerror("Error", "Select a tournament first.")
            return

        name = self.tourn_name_var.get()
        date = self.start_date_var.get()
        prize = self.prize_var.get()

        db = connect_db()
        cursor = db.cursor()
        cursor.execute("""
            UPDATE TOURNAMENT
            SET Tourn_Name=%s, Start_Date=%s, Prize_Pool=%s
            WHERE Tourn_ID=%s
        """, (name, date, prize, tid))
        db.commit()
        db.close()

        self.load_tournaments()
        self.clear_fields()
        messagebox.showinfo("Success", "Tournament updated!")

    def delete_tournament(self):
        tid = self.tourn_id_var.get()
        if tid == "":
            messagebox.showerror("Error", "Select a tournament first.")
            return

        if not messagebox.askyesno("Confirm", "Delete this tournament?"):
            return

        db = connect_db()
        cursor = db.cursor()
        cursor.execute("DELETE FROM TOURNAMENT WHERE Tourn_ID=%s", (tid,))
        db.commit()
        db.close()

        self.load_tournaments()
        self.clear_fields()
        messagebox.showinfo("Success", "Tournament deleted!")

    # ---------------- UI HELPERS ---------------- #

    def clear_fields(self):
        self.tourn_id_var.set("")
        self.tourn_name_var.set("")
        self.start_date_var.set("")
        self.prize_var.set("")

    def select_tournament(self, event):
        row = self.tree.focus()
        if not row:
            return

        data = self.tree.item(row)["values"]

        self.tourn_id_var.set(data[0])
        self.tourn_name_var.set(data[1])
        self.start_date_var.set(data[2])
        self.prize_var.set(data[3])


# --- 3. MATCHES Management Window (CRUD) ---

class MatchManager(tk.Toplevel):
    """
    Implements a full CRUD interface for the MATCHES table.
    Uses dropdowns for Foreign Keys (Team and Tournament).
    """
    def __init__(self, master):
        super().__init__(master)
        self.title("Record Match Results (CRUD on MATCHES)")
        self.geometry("900x650")
        self.db_conn = connect_db()
        self.team_options = get_team_ids_names(self.db_conn)
        self.tourn_options = get_tournament_ids_names(self.db_conn)
        self.match_id_pk = None # Store PK of selected match
        
        self.create_widgets()
        self.load_data()

    def _get_id_from_selection(self, selection_str):
        """Utility to extract the ID (e.g., 'SEN') from a combo string ('SEN - Sentinels')."""
        if not selection_str: return None
        return selection_str.split(' - ')[0]

    def _get_match_winner_options(self):
        """Dynamically generates options for the Winner dropdown (Team A, Team B, or None)."""
        options = [""] # Option for no winner/tie (NULL in DB)
        
        team_a_str = self.team_a_combo.get()
        team_b_str = self.team_b_combo.get()

        if team_a_str: options.append(team_a_str)
        if team_b_str and team_b_str != team_a_str: options.append(team_b_str)
        
        return options
    
    def create_widgets(self):
        """Sets up the layout, input fields, and display area for Matches."""
        
        # --- 3.1 Input Frame (Top) ---
        input_frame = ttk.LabelFrame(self, text="Match Details", padding="10")
        input_frame.pack(padx=10, pady=10, fill="x")

        # Row 0: Tournament
        tk.Label(input_frame, text="Tournament ID:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.tourn_combo = ttk.Combobox(input_frame, values=self.tourn_options, state="readonly", width=30)
        self.tourn_combo.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        
        # Row 1: Team A and Score A
        tk.Label(input_frame, text="Team A:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.team_a_combo = ttk.Combobox(input_frame, values=self.team_options, state="readonly", width=30)
        self.team_a_combo.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        self.team_a_combo.bind("<<ComboboxSelected>>", lambda e: self.update_winner_options())

        tk.Label(input_frame, text="Score A:").grid(row=1, column=2, padx=5, pady=5, sticky="w")
        self.score_a_entry = tk.Entry(input_frame, width=5)
        self.score_a_entry.grid(row=1, column=3, padx=5, pady=5, sticky="w")

        # Row 2: Team B and Score B
        tk.Label(input_frame, text="Team B:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.team_b_combo = ttk.Combobox(input_frame, values=self.team_options, state="readonly", width=30)
        self.team_b_combo.grid(row=2, column=1, padx=5, pady=5, sticky="w")
        self.team_b_combo.bind("<<ComboboxSelected>>", lambda e: self.update_winner_options())

        tk.Label(input_frame, text="Score B:").grid(row=2, column=2, padx=5, pady=5, sticky="w")
        self.score_b_entry = tk.Entry(input_frame, width=5)
        self.score_b_entry.grid(row=2, column=3, padx=5, pady=5, sticky="w")

        # Row 3: Winner
        tk.Label(input_frame, text="Winner:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.winner_combo = ttk.Combobox(input_frame, values=[""], state="readonly", width=30)
        self.winner_combo.grid(row=3, column=1, padx=5, pady=5, sticky="w")

        # --- 3.2 CRUD Buttons ---
        button_frame = ttk.Frame(self)
        button_frame.pack(padx=10, pady=5)

        ttk.Button(button_frame, text="Record Match (Create)", command=self.add_match).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Update Selected (Update)", command=self.update_match).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Delete Selected (Delete)", command=self.delete_match).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Clear Form", command=self.clear_form).pack(side=tk.LEFT, padx=5)

        # --- 3.3 Data Display Area (Bottom) ---
        columns = ("ID", "Tournament", "Team A", "Team B", "Winner", "Score A", "Score B")
        self.tree = ttk.Treeview(self, columns=columns, show="headings")
        self.tree.pack(padx=10, pady=10, fill="both", expand=True)

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center")
        self.tree.column("ID", width=40)
        self.tree.column("Tournament", width=150)

        self.tree.bind('<<TreeviewSelect>>', self.select_item)

    def update_winner_options(self):
        """Updates the winner dropdown based on the selected Team A and Team B."""
        current_winner = self.winner_combo.get()
        new_options = self._get_match_winner_options()
        
        self.winner_combo['values'] = new_options
        
        # Try to keep the current selection if it's still valid
        if current_winner in new_options:
            self.winner_combo.set(current_winner)
        else:
            self.winner_combo.set("")

    def clear_form(self):
        """Clears all input fields and resets internal state."""
        self.tourn_combo.set("")
        self.team_a_combo.set("")
        self.team_b_combo.set("")
        self.winner_combo.set("")
        self.score_a_entry.delete(0, tk.END)
        self.score_b_entry.delete(0, tk.END)
        self.match_id_pk = None

    def select_item(self, event):
        """When a row is selected, populate the form for potential update/delete."""
        selected_item = self.tree.focus()
        if not selected_item:
            return

        values = self.tree.item(selected_item, 'values')
        self.clear_form()

        # Store PK
        self.match_id_pk = values[0]

        # Populate Comboboxes (values[1] through values[4] are the full descriptive strings)
        self.tourn_combo.set(values[1])
        self.team_a_combo.set(values[2])
        self.team_b_combo.set(values[3])
        
        # Update winner options based on selected teams, then set winner
        self.update_winner_options()
        self.winner_combo.set(values[4])

        # Populate Scores
        self.score_a_entry.insert(0, values[5])
        self.score_b_entry.insert(0, values[6])
        
    # --- 3.4 CRUD Implementations (Using the correct 'MATCHES' table) ---

    def load_data(self):
        """R (Read) - Retrieves all records and displays them in the Treeview."""
        for item in self.tree.get_children():
            self.tree.delete(item) 
            
        if not self.db_conn: return

        cursor = self.db_conn.cursor()
        
        # SQL query joins tables to fetch names instead of just IDs for better readability
        query = """
        SELECT 
            M.Match_ID, 
            CONCAT(T.Tourn_ID, ' - ', T.Tourn_Name) AS Tournament, 
            CONCAT(TA.Team_ID, ' - ', TA.Team_Name) AS TeamA, 
            CONCAT(TB.Team_ID, ' - ', TB.Team_Name) AS TeamB,
            CASE 
                WHEN M.Winner_ID IS NULL THEN 'None' 
                ELSE CONCAT(W.Team_ID, ' - ', W.Team_Name) 
            END AS Winner,
            M.Score_A, 
            M.Score_B 
        FROM MATCHES M
        JOIN TOURNAMENT T ON M.Tourn_ID = T.Tourn_ID
        JOIN TEAM TA ON M.Team_A_ID = TA.Team_ID
        JOIN TEAM TB ON M.Team_B_ID = TB.Team_ID
        LEFT JOIN TEAM W ON M.Winner_ID = W.Team_ID;
        """
        try:
            cursor.execute(query)
            for row in cursor.fetchall():
                self.tree.insert('', tk.END, values=row)
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Failed to load match data: {err}")
        finally:
            cursor.close()

    def add_match(self):
        """C (Create) - Inserts a new match record into MATCHES."""
        
        # Extract IDs from the combobox full strings (e.g., 'SEN - Sentinels' -> 'SEN')
        tourn_id = self._get_id_from_selection(self.tourn_combo.get())
        team_a_id = self._get_id_from_selection(self.team_a_combo.get())
        team_b_id = self._get_id_from_selection(self.team_b_combo.get())
        winner_id = self._get_id_from_selection(self.winner_combo.get())
        
        score_a = self.score_a_entry.get()
        score_b = self.score_b_entry.get()

        if not all([tourn_id, team_a_id, team_b_id, score_a, score_b]):
            messagebox.showwarning("Input Error", "Tournament, both Teams, and both Scores are required.")
            return

        if team_a_id == team_b_id:
            messagebox.showwarning("Input Error", "Team A and Team B must be different teams.")
            return

        if not self.db_conn: return
        cursor = self.db_conn.cursor()
        
        sql = """
        INSERT INTO matches (Tourn_ID, Team_A_ID, Team_B_ID, Winner_ID, Score_A, Score_B) 
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        try:
            cursor.execute(sql, (tourn_id, team_a_id, team_b_id, winner_id, score_a, score_b))
            self.db_conn.commit()
            messagebox.showinfo("Success", "Match recorded successfully.")
            self.clear_form()
            self.load_data() 
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Failed to record match: {err}")
        finally:
            cursor.close()

    def update_match(self):
        """U (Update) - Updates the selected match record."""
        if self.match_id_pk is None:
            messagebox.showwarning("Selection Error", "Please select a match to update.")
            return

        # Extract IDs from the combobox full strings
        tourn_id = self._get_id_from_selection(self.tourn_combo.get())
        team_a_id = self._get_id_from_selection(self.team_a_combo.get())
        team_b_id = self._get_id_from_selection(self.team_b_combo.get())
        winner_id = self._get_id_from_selection(self.winner_combo.get())
        
        score_a = self.score_a_entry.get()
        score_b = self.score_b_entry.get()

        if not all([tourn_id, team_a_id, team_b_id, score_a, score_b]):
            messagebox.showwarning("Input Error", "All fields except Winner are required.")
            return
        
        if team_a_id == team_b_id:
            messagebox.showwarning("Input Error", "Team A and Team B must be different teams.")
            return

        if not self.db_conn: return
        cursor = self.db_conn.cursor()

        sql = """
        UPDATE matches 
        SET Tourn_ID = %s, Team_A_ID = %s, Team_B_ID = %s, Winner_ID = %s, Score_A = %s, Score_B = %s
        WHERE Match_ID = %s
        """
        try:
            cursor.execute(sql, (tourn_id, team_a_id, team_b_id, winner_id, score_a, score_b, self.match_id_pk))
            self.db_conn.commit()
            messagebox.showinfo("Success", f"Match ID {self.match_id_pk} updated successfully.")
            self.clear_form()
            self.load_data() 
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Failed to update match: {err}")
        finally:
            cursor.close()

    def delete_match(self):
        """D (Delete) - Deletes the selected match record."""
        if self.match_id_pk is None:
            messagebox.showwarning("Selection Error", "Please select a match to delete.")
            return
        
        match_info = f"Match ID {self.match_id_pk}"

        if not messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete {match_info}?"):
            return

        if not self.db_conn: return
        cursor = self.db_conn.cursor()
        
        sql = "DELETE FROM matches WHERE Match_ID = %s"
        try:
            cursor.execute(sql, (self.match_id_pk,))
            self.db_conn.commit()
            messagebox.showinfo("Success", f"{match_info} deleted successfully.")
            self.clear_form()
            self.load_data() 
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Failed to delete match: {err}")
        finally:
            cursor.close()

# ---  REPORT WINDOW ---
class ReportGenerator(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)

        # Window settings
        self.title("Generate Reports")
        self.geometry("600x450")
        self.configure(bg="#0f1923")

        # Title
        tk.Label(
            self,
            text="Report Generator",
            font=("Helvetica", 18, "bold"),
            bg="#0f1923",
            fg="white"
        ).pack(pady=15)

        # Frame for options
        options_frame = tk.Frame(self, bg="#0f1923")
        options_frame.pack(pady=10)

        # Buttons (add more anytime)
        report_buttons = [
            ("Player List Report", self.generate_player_report),
            ("Team List Report", self.generate_team_report),
            ("Tournament Summary Report", self.generate_tournament_report),
            ("Prize Pool Rankings", self.generate_prizepool_report)
        ]

        for text, command in report_buttons:
            tk.Button(
                options_frame,
                text=text,
                command=command,
                bg="#ff4655",
                fg="white",
                width=30,
                height=2
            ).pack(pady=8)

        # Output box (for preview)
        tk.Label(self, text="Report Output", bg="#0f1923", fg="white").pack(pady=5)
        self.output_text = tk.Text(self, height=8, width=60)
        self.output_text.pack(padx=10, pady=10)

    # ---------------------------
    # REPORT FUNCTIONS
    # ---------------------------
    def generate_player_report(self):
        self.output_text.delete("1.0", tk.END)
        self.output_text.insert(tk.END, "=== PLAYER REPORT ===\n\n")

        db = connect_db()
        if not db:
            self.output_text.insert(tk.END, "❌ Unable to connect to database.")
            return

        cursor = db.cursor()
        cursor.execute("""
            SELECT P.Player_ID, P.IGN, P.Real_Name,
                COALESCE(T.Team_Name, 'No Team')
            FROM PLAYER P
            LEFT JOIN TEAM T ON P.Team_ID = T.Team_ID
            ORDER BY P.IGN ASC;
        """)
        rows = cursor.fetchall()

        for row in rows:
            self.output_text.insert(
                tk.END,
                f"ID: {row[0]} | IGN: {row[1]} | Name: {row[2]} | Team: {row[3]}\n"
            )

        cursor.close()
        db.close()
    def generate_team_report(self):
        self.output_text.delete("1.0", tk.END)
        self.output_text.insert(tk.END, "=== TEAM REPORT ===\n\n")

        db = connect_db()
        if not db:
            self.output_text.insert(tk.END, "❌ Unable to connect to database.")
            return

        cursor = db.cursor()
        cursor.execute("""
            SELECT Team_ID, Team_Name, Coach_Name
            FROM TEAM
            ORDER BY Team_Name ASC;
        """)
        rows = cursor.fetchall()

        for row in rows:
            self.output_text.insert(
                tk.END,
                f"{row[0]} | {row[1]} | Coach: {row[2]}\n"
            )

        cursor.close()
        db.close()
    def generate_tournament_report(self):
        self.output_text.delete("1.0", tk.END)
        self.output_text.insert(tk.END, "=== TOURNAMENT SUMMARY ===\n\n")

        db = connect_db()
        if not db:
            self.output_text.insert(tk.END, "❌ Unable to connect to database.")
            return

        cursor = db.cursor()
        cursor.execute("""
            SELECT Tourn_ID, Tourn_Name, Start_Date, Prize_Pool
            FROM TOURNAMENT
            ORDER BY Start_Date DESC;
        """)
        rows = cursor.fetchall()

        for row in rows:
            self.output_text.insert(
                tk.END,
                f"{row[0]} | {row[1]} | Start: {row[2]} | Prize: ₱{row[3]:,.2f}\n"
            )

        cursor.close()
        db.close()
    def generate_prizepool_report(self):
        self.output_text.delete("1.0", tk.END)
        self.output_text.insert(tk.END, "=== PRIZE POOL RANKINGS ===\n\n")

        db = connect_db()
        if not db:
            self.output_text.insert(tk.END, "❌ Unable to connect to database.")
            return

        cursor = db.cursor()
        cursor.execute("""
            SELECT Tourn_Name, Prize_Pool
            FROM TOURNAMENT
            ORDER BY Prize_Pool DESC;
        """)
        rows = cursor.fetchall()

        rank = 1
        for row in rows:
            self.output_text.insert(
                tk.END,
                f"{rank}. {row[0]} - ₱{row[1]:,.2f}\n"
            )
            rank += 1

        cursor.close()
        db.close()


# --- 4. Main Application Class ---

class ValorantTrackerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("VEMT: Valorant Esports Match Tracker")
        self.geometry("450x350")
        self.configure(bg="#2d2d2d") # Dark background for Valorant aesthetic

        self.style = ttk.Style(self)
        self.style.theme_use('clam')
        # Customizing button style for a red/black Valorant theme
        self.style.configure("TButton", padding=10, font=('Arial', 10, 'bold'), 
                             background='#c91f37', foreground='white', borderwidth=0)
        self.style.map("TButton", background=[('active', '#e6324d')])
        self.style.configure("TLabel", background="#2d2d2d", foreground='white')
        self.style.configure("TFrame", background="#2d2d2d")
        self.style.configure("TLabelframe", background="#2d2d2d", foreground='white')
        self.style.configure("TLabelframe.Label", background="#2d2d2d", foreground='white', font=('Arial', 10, 'bold'))


        self.create_main_menu()

    def create_main_menu(self):
        """Creates the main navigation window."""
        main_frame = ttk.Frame(self, padding="20 20 20 20")
        main_frame.pack(expand=True, fill="both")
        
        # Title
        ttk.Label(main_frame, text="VEMT: Valorant Tracker", 
                    font=("Arial", 18, 'bold'), foreground="#c91f37").pack(pady=15)
        
        # Navigation Buttons
        ttk.Button(main_frame, text="1. Manage Teams", 
                    command=lambda: self.open_window(TeamManager)).pack(fill='x', pady=5)
                    
        ttk.Button(main_frame, text="2. Manage Players", 
                    command=lambda: self.open_window(PlayerManager)).pack(fill='x', pady=5)
                    
        ttk.Button(main_frame, text="3. Manage Tournaments", 
                    command=lambda: self.open_window(TournamentManager)).pack(fill='x', pady=5)
                    
        ttk.Button(main_frame, text="4. Record Match Results", 
                    command=lambda: self.open_window(MatchManager)).pack(fill='x', pady=5) # Now opens the new class
                    
        ttk.Button(main_frame, text="5. Generate Reports", 
                    command=lambda: self.open_window(ReportGenerator)).pack(fill='x', pady=5)

    def open_window(self, WindowClass):
        """Opens a new top-level window for a specific management task."""
        # This prevents opening multiple windows of the same type
        if any(isinstance(w, WindowClass) for w in self.winfo_children()):
            return 
        WindowClass(self)

if __name__ == "__main__":
    app = ValorantTrackerApp()
    app.mainloop()