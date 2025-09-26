# runclient.ps1

# Pobierz zależności
pip install -e ".[ai]"

# 3. Odpal klienta
$env:PYTHONPATH="src"
python client_tk.py --host 10.71.81.2 --port 8000

