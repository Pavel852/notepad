import tkinter as tk
from tkinter import filedialog, messagebox
import configparser

class Notepad:
    def __init__(self, root):
        self.root = root
        self.root.title("NotePad")
        self.root.geometry("800x600")

        # Načtení textů z lang.ini (UTF-8)
        self.config = configparser.ConfigParser()
        self.config.read("lang.ini", encoding="utf-8")  # nebo "utf-8-sig", pokud je v souboru BOM
        self.lang = self.config["cs"]  # Předpokládáme sekci [cs]

        # Rám pro line numbers (vlevo) a hlavní text (vpravo)
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill='both', expand=True)

        # Proměnná pro zobrazení čísel řádků
        self.line_numbers_visible = False

        # Proměnná pro zobrazení statistik v liště
        self.show_stats_in_status_bar = False

        # Text pro čísla řádků
        self.line_numbers = tk.Text(
            self.main_frame,
            width=4,
            padx=5,
            takefocus=0,
            border=0,
            background='#f0f0f0',
            state='disabled'
        )
        # Nezobrazujeme hned – zobrazí se až při přepnutí

        # Hlavní textové pole
        self.text_area = tk.Text(self.main_frame, wrap='word')
        self.text_area.pack(side='right', expand=True, fill='both')
        self.text_area.bind("<KeyRelease>", self.on_text_change)

        # Vytvoření menu
        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)

        # Menu Soubor
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(
            label=self.lang["menu_soubor"], 
            menu=self.file_menu
        )
        self.file_menu.add_command(
            label=self.lang["menu_novy"], 
            command=self.new_file
        )
        self.file_menu.add_command(
            label=self.lang["menu_otevrit"], 
            command=self.open_file
        )
        self.file_menu.add_command(
            label=self.lang["menu_ulozit"], 
            command=self.save_file
        )
        self.file_menu.add_command(
            label=self.lang["menu_ulozit_jako"],
            command=self.save_file_as
        )
        self.file_menu.add_separator()
        self.file_menu.add_command(
            label=self.lang["menu_ukoncit"], 
            command=self.exit_editor
        )

        # Menu Úpravy
        self.edit_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(
            label=self.lang["menu_upravy"], 
            menu=self.edit_menu
        )
        self.edit_menu.add_command(
            label=self.lang["menu_vyjmout"], 
            command=self.cut_text
        )
        self.edit_menu.add_command(
            label=self.lang["menu_kopirovat"], 
            command=self.copy_text
        )
        self.edit_menu.add_command(
            label=self.lang["menu_vlozit"], 
            command=self.paste_text
        )
        self.edit_menu.add_command(
            label=self.lang["menu_vlozit_symbol"],
            command=self.insert_symbol
        )

        # Menu Zobrazení
        self.view_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(
            label=self.lang["menu_zobrazeni"], 
            menu=self.view_menu
        )
        self.view_menu.add_command(
            label=self.lang["menu_cisla_radku"], 
            command=self.toggle_line_numbers
        )
        self.view_menu.add_command(
            label=self.lang["menu_statistika"], 
            command=self.show_statistics_dialog
        )
        self.view_menu.add_command(
            label=self.lang["menu_statistika_lista"],
            command=self.toggle_statistics_in_status_bar
        )

        # Menu Kódování
        self.encoding_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(
            label=self.lang["menu_kodovani"], 
            menu=self.encoding_menu
        )

        # Přidáme seznam kódování (13 celkem: 3 původní + 10 nových)
        encodings = [
            ('UTF-8', 'utf-8'),
            ('Windows-1250', 'windows-1250'),
            ('CP852', 'cp852'),
            ('ISO-8859-1', 'iso-8859-1'),
            ('ISO-8859-2', 'iso-8859-2'),
            ('ISO-8859-15', 'iso-8859-15'),
            ('Windows-1252', 'windows-1252'),
            ('ASCII', 'ascii'),
            ('Shift_JIS', 'shift_jis'),
            ('EUC-JP', 'euc_jp'),
            ('GB2312', 'gb2312'),
            ('BIG5', 'big5'),
            ('KOI8-R', 'koi8-r')
        ]
        for enc_label, enc_val in encodings:
            self.encoding_menu.add_command(
                label=enc_label,
                command=lambda e=enc_val: self.set_encoding(e)
            )

        # Menu Nápověda
        self.help_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(
            label=self.lang["menu_napoveda"], 
            menu=self.help_menu
        )
        self.help_menu.add_command(
            label=self.lang["menu_o_programu"], 
            command=self.show_about
        )

        # Výchozí kódování
        self.current_encoding = 'utf-8'

        # Proměnná pro aktuální soubor
        self.file_path = None

        # Status bar (patička)
        self.status_bar = tk.Label(self.root, text="Author: PB", anchor='e')
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    # ========== SOUBOR ==========

    def new_file(self):
        self.text_area.delete(1.0, tk.END)
        self.file_path = None
        self.root.title("Nový soubor - Jednoduchý Textový Editor")

    def open_file(self):
        self.file_path = filedialog.askopenfilename(
            defaultextension=".txt",
            filetypes=[("Textové soubory", "*.txt"), ("Všechny soubory", "*.*")]
        )
        if self.file_path:
            try:
                with open(self.file_path, "r", encoding=self.current_encoding) as file:
                    content = file.read()
                    self.text_area.delete(1.0, tk.END)
                    self.text_area.insert(tk.END, content)
                    self.root.title(f"{self.file_path} - Jednoduchý Textový Editor")
            except (UnicodeDecodeError, LookupError):
                messagebox.showerror(
                    "Chyba",
                    f"Nelze otevřít soubor s kódováním {self.current_encoding}."
                )

    def save_file(self):
        """Uloží soubor (pokud není cesta, vyvolá dialog)."""
        if self.file_path is None:
            # Pokud není definována cesta, použijeme "Uložit jako..."
            return self.save_file_as()
        else:
            self._save_to_path(self.file_path)

    def save_file_as(self):
        """Vždy vyvolá dialog a uloží do zvolené cesty."""
        path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Textové soubory", "*.txt"), ("Všechny soubory", "*.*")]
        )
        if not path:
            return  # uživatel zrušil
        self._save_to_path(path)

    def _save_to_path(self, path):
        """Pomocná metoda pro skutečné uložení do souboru."""
        try:
            with open(path, "w", encoding=self.current_encoding) as file:
                content = self.text_area.get(1.0, tk.END)
                file.write(content)
            self.file_path = path
            self.root.title(f"{self.file_path} - Jednoduchý Textový Editor")
        except (UnicodeEncodeError, LookupError):
            messagebox.showerror(
                "Chyba",
                f"Nelze uložit soubor s kódováním {self.current_encoding}."
            )

    def exit_editor(self):
        if messagebox.askokcancel("Ukončit", "Opravdu chcete ukončit editor?"):
            self.root.destroy()

    # ========== ÚPRAVY ==========

    def cut_text(self):
        self.text_area.event_generate("<<Cut>>")

    def copy_text(self):
        self.text_area.event_generate("<<Copy>>")

    def paste_text(self):
        self.text_area.event_generate("<<Paste>>")

    def insert_symbol(self):
        """Otevře okno s výběrem symbolu a vloží ho do textu."""
        symbols = ["©", "®", "™", "…", "—", "€", "¶", "∞", "♥", "→"]

        # Vytvořit nové top-level okno
        symbol_window = tk.Toplevel(self.root)
        symbol_window.title("Vložit symbol")

        # Popisek
        tk.Label(symbol_window, text="Vyberte symbol:").pack(padx=10, pady=5)

        # Listbox se symboly
        listbox = tk.Listbox(symbol_window, height=len(symbols))
        listbox.pack(padx=10, pady=5)

        # Naplnit listbox
        for sym in symbols:
            listbox.insert(tk.END, sym)

        # Funkce, která vloží vybraný symbol do textu
        def on_symbol_select(event):
            selection = listbox.curselection()
            if selection:
                index = selection[0]
                symbol = symbols[index]
                # Vložit symbol do text_area na aktuální pozici
                self.text_area.insert(tk.INSERT, symbol)
                symbol_window.destroy()

        # Poklepáním vložit symbol
        listbox.bind("<Double-Button-1>", on_symbol_select)

    # ========== ZOBRAZENÍ ==========

    def toggle_line_numbers(self):
        """Zapne/vypne zobrazení čísel řádků."""
        self.line_numbers_visible = not self.line_numbers_visible
        if self.line_numbers_visible:
            self.line_numbers.pack(side='left', fill='y')
            self.update_line_numbers()
        else:
            self.line_numbers.pack_forget()

    def show_statistics_dialog(self):
        """Zobrazí statistiku (řádky, slova, znaky) v dialogu."""
        text_content = self.text_area.get(1.0, tk.END).rstrip('\n')
        lines = text_content.split('\n')
        words = text_content.split()
        chars = len(text_content)

        msg = (
            f"Počet řádků: {len(lines)}\n"
            f"Počet slov: {len(words)}\n"
            f"Počet znaků: {chars}"
        )
        messagebox.showinfo("Statistika", msg)

    def toggle_statistics_in_status_bar(self):
        """Zapíná/vypíná zobrazování statistik v dolní liště."""
        self.show_stats_in_status_bar = not self.show_stats_in_status_bar
        # Ihned aktualizovat lištu
        self.update_status_bar()

    # ========== KÓDOVÁNÍ ==========

    def set_encoding(self, encoding):
        self.current_encoding = encoding
        messagebox.showinfo("Kódování", f"Nastaveno kódování: {self.current_encoding}")

    # ========== NÁPOVĚDA ==========

    def show_about(self):
        about_message = (
            "Jednoduchý Textový Editor\n"
            "Verze: 1.0\n"
            "Licence: CC\n"
            "Autor: PB\n"
            "Email: pavel.bartos.pb@gmail.com\n"
            "Rok: 01/2025"
        )
        messagebox.showinfo("O programu", about_message)

    # ========== DOPLŇKOVÉ FUNKCE ==========

    def on_text_change(self, event=None):
        """Volá se při každém uvolnění klávesy. Aktualizuje čísla řádků i status bar."""
        self.update_line_numbers()
        self.update_status_bar()

    def update_line_numbers(self):
        """Aktualizuje čísla řádků, pokud jsou zapnutá."""
        if not self.line_numbers_visible:
            return

        # Počet řádků
        line_count = int(self.text_area.index('end-1c').split('.')[0])

        self.line_numbers.config(state='normal')
        self.line_numbers.delete('1.0', tk.END)

        for i in range(1, line_count + 1):
            self.line_numbers.insert(tk.END, f"{i}\n")

        self.line_numbers.config(state='disabled')

    def update_status_bar(self):
        """
        Pokud je show_stats_in_status_bar=True, ukazuje statistiku v liště.
        Jinak jen 'Author: PB'.
        """
        if self.show_stats_in_status_bar:
            text_content = self.text_area.get(1.0, tk.END).rstrip('\n')
            lines = text_content.split('\n')
            words = text_content.split()
            chars = len(text_content)

            status_text = (
                f"Řádků: {len(lines)}, "
                f"Slov: {len(words)}, "
                f"Znaků: {chars}  |  Author: PB"
            )
            self.status_bar.config(text=status_text)
        else:
            self.status_bar.config(text="Author: PB")


if __name__ == "__main__":
    root = tk.Tk()
    root.iconbitmap('notepad.ico')
    notepad = Notepad(root)
    root.mainloop()
