# runclient.ps1

# 1. Otwórz tunel SSH na porcie 8000
Start-Process powershell -ArgumentList '-NoExit', '-Command', 'ssh -NL localhost:8000:localhost:8000 s490115@g1n2.cluster.wmi.amu.edu.pl'

# 2. Poczekaj chwilę, aż tunel się zestawi
Start-Sleep -Seconds 3

# 3. Odpal klienta
$env:PYTHONPATH="src"
python client_tk.py --host localhost --port 8000