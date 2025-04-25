import mysql.connector
import tkinter as tk
from tkinter import messagebox, simpledialog

# --- Database Configuration ---
def get_connection():
    """
    Create and return a new connection to the MySQL database.
    Assumes 'voting_db' and tables already exist.
    """
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="MySQL_Root#7945!",
        database="voting_db",
        port=3306
    )

# --- Candidate Operations ---
def add_candidate(name: str, party: str) -> None:
    """
    Insert a new candidate into the database.
    """
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO candidates (name, party) VALUES (%s, %s)",
                (name.strip(), party.strip())
            )
        conn.commit()


def list_candidates() -> list:
    """
    Retrieve all candidates, ordered by ID.
    Returns a list of tuples: (id, name, party).
    """
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT id, name, party FROM candidates ORDER BY id"
            )
            return cursor.fetchall()


def delete_candidate(candidate_id: int) -> None:
    """
    Remove a candidate and any associated votes.
    """
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "DELETE FROM votes WHERE candidate_id = %s", (candidate_id,)
            )
            cursor.execute(
                "DELETE FROM candidates WHERE id = %s", (candidate_id,)
            )
        conn.commit()

# --- Voting Operations ---
def cast_vote(candidate_id: int) -> None:
    """
    Record a vote for the given candidate ID.
    """
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO votes (candidate_id) VALUES (%s)",
                (candidate_id,)
            )
        conn.commit()


def view_results() -> list:
    """
    Get current vote counts for all candidates.
    Returns a list of tuples: (name, party, vote_count).
    """
    query = (
        "SELECT c.name, c.party, COUNT(v.id) "
        "FROM candidates c "
        "LEFT JOIN votes v ON c.id = v.candidate_id "
        "GROUP BY c.id "
        "ORDER BY c.id"
    )
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query)
            return cursor.fetchall()

# --- GUI Setup with Continuous Numbering ---
def main_menu():
    """
    Build and display the main application window.
    Uses list indices for display so numbering remains continuous.
    """
    root = tk.Tk()
    root.title("Voting App")

    # Listbox to display candidates
    candidate_list = tk.Listbox(root, width=50)
    candidate_list.pack(pady=10)

    # This list holds candidate IDs in the order shown
    candidate_ids = []

    def refresh_candidates():
        """Reload the candidate list with continuous numbering."""
        candidate_list.delete(0, tk.END)
        candidate_ids.clear()
        rows = list_candidates()
        # Display with enumeration to avoid gaps
        for index, (cid, name, party) in enumerate(rows, start=1):
            candidate_list.insert(tk.END, f"{index}. {name} ({party})")
            candidate_ids.append(cid)

    def handle_add():
        """Prompt user to add a new candidate."""
        name = simpledialog.askstring("Add Candidate", "Candidate name:")
        party = simpledialog.askstring("Add Candidate", "Candidate party:")
        if name and party:
            add_candidate(name, party)
            refresh_candidates()
            messagebox.showinfo("Success", "Candidate added.")

    def handle_vote():
        """Record a vote for the selected candidate by list position."""
        try:
            sel = candidate_list.curselection()
            if not sel:
                raise IndexError
            # Map displayed index to actual candidate ID
            idx = sel[0]
            cid = candidate_ids[idx]
            cast_vote(cid)
            messagebox.showinfo("Success", "Vote recorded.")
        except (IndexError, ValueError):
            messagebox.showerror("Error", "Select a candidate first.")

    def handle_results():
        """Show voting results in an info dialog."""
        results = view_results()
        text = "\n".join(f"{name} ({party}) - {count} votes" for name, party, count in results)
        messagebox.showinfo("Results", text)

    def handle_delete():
        """Delete the selected candidate after confirmation."""
        try:
            sel = candidate_list.curselection()
            if not sel:
                raise IndexError
            idx = sel[0]
            cid = candidate_ids[idx]
            if messagebox.askyesno("Confirm", "Delete this candidate? This will remove all their votes."):
                delete_candidate(cid)
                refresh_candidates()
                messagebox.showinfo("Deleted", "Candidate removed.")
        except (IndexError, ValueError):
            messagebox.showerror("Error", "Select a candidate to delete.")

    # Buttons
    tk.Button(root, text="Refresh Candidates", command=refresh_candidates).pack(pady=2)
    tk.Button(root, text="Add Candidate", command=handle_add).pack(pady=2)
    tk.Button(root, text="Vote", command=handle_vote).pack(pady=2)
    tk.Button(root, text="View Results", command=handle_results).pack(pady=2)
    tk.Button(root, text="Delete Candidate", command=handle_delete).pack(pady=2)
    tk.Button(root, text="Exit", command=root.destroy).pack(pady=5)

    # Initialize list and start
    refresh_candidates()
    root.mainloop()

if __name__ == "__main__":
    main_menu()
