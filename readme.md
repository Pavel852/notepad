========================================
Jednoduchý Textový Editor (notepad.py)
========================================

Autor:
  PB

Licence:
  Creative Commons (CC)

Popis:
  Tento jednoduchý textový editor slouží k vytváření, otevírání a ukládání
  textových souborů, podporuje zobrazení čísel řádků, vkládání symbolů,
  volbu kódování, zobrazování statistik (počet řádků, slov a znaků),
  a další funkce.

----------------------------------------
Jak spustit (bez kompilace)
----------------------------------------
1. Ujistěte se, že máte nainstalovaný Python 3.x.
2. V příkazové řádce (terminálu) zadejte:
   
   python notepad.py

----------------------------------------
Kompilace do spustitelného souboru
----------------------------------------
Kompilace probíhá pomocí nástroje PyInstaller. Nejprve je nutné jej nainstalovat:

  pip install pyinstaller

----------------------------------------
1) Windows (.exe)
----------------------------------------
1. V příkazové řádce na Windows zadejte:

   pyinstaller --onefile --windowed --icon=notepad.ico notepad.py

2. Vyčkejte dokončení kompilace. Ve složce "dist" se pak objeví soubor
   "notepad.exe", který lze spouštět samostatně.

----------------------------------------
2) Linux (ELF binární soubor)
----------------------------------------
1. V terminálu na Linuxu zadejte:

   pyinstaller --onefile --windowed --icon=notepad.ico notepad.py

2. Po dokončení kompilace se ve složce "dist" objeví spustitelný soubor
   "notepad" (bez přípony), který lze spustit příkazem:

   ./dist/notepad

----------------------------------------
Poznámky:
----------------------------------------
- Při kompilaci může být nutné doinstalovat další závislosti (např. Tkinter
  je obvykle součástí standardní knihovny Pythonu, ale někdy je vyžadován
  balíček navíc).
- Soubor notepad.ico není povinný, pokud nevyžadujete ikonu, lze parametr
  "--icon=..." vynechat.

----------------------------------------
Autor & Licence:
----------------------------------------
- Autor: PB
- Licence: Creative Commons (CC)
