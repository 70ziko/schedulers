import argparse
import numpy as np
import sys
import generator
import schedulers
import pagefile

# obsługa programu poprzez argumenty przekazywane w konsoli
parser = argparse.ArgumentParser(description='Symulator algorytmów planowania czasu procesora or zastępowania stron. \nGdy nie ma wybranej żadnej opcji symuluje FCFS')
parser.add_argument('-p','--path', type=str , help='Podaj ścieżkę pliku źródłowego lub liczbę procesów do wygenerowania (domyślnie = 20)', default='20')
parser.add_argument('-m','--mean', type=int , help='Przekaż do generatora średni czas wykonania (domyślnie = 20)', default=20)
parser.add_argument('-s','--scale', type=int , help='Przekaż do generatora odchylenie standardowe (domyślnie = 5)', default=5)
parser.add_argument('-f', '--frames', type=int, help='Podaj ilość ramek dla algorytmów zastępowania stron (domyślnie = 5)', default=5)
parser.add_argument('--random' , help='Generuj procesy losowo, domyślnie generuje procesy w rozkładzie normalnym', action='store_true')
parser.add_argument('--upp', type=int, help='Podaj górną granicę generowanych danych (domyślnie taka jak liczba procesów do generowania)', default=-1)
parser.add_argument('--zeroes' , help='Generuj procesy o czasie przyjścia równym 0', action='store_true')
parser.add_argument('--FCFS', help='Symuluj algorytm First Come First Serve', action='store_true')
parser.add_argument('--SJF', help='Symuluj algorytm Shortest Job First', action='store_true')
parser.add_argument('--FIFO', help='Symuluj algorytm First In First Out', action='store_true')
parser.add_argument('--LRU', help='Symuluj algorytm Least Recently Used', action='store_true')
parser.add_argument('--LFU', help='Symuluj algorytm Least Frequently Used --- ZBUGOWANE, UŻYWAĆ NA WŁASNĄ ODPOWIEDZIALNOŚĆ!!!', action='store_true')
args=parser.parse_args()

# ustawianie domyślnej granicy generatora
if args.path.isnumeric() and args.upp == -1:
    args.upp = int(args.path)

# odczytywanie lub generowanie listy procesów
processes = np.array([])
if args.path.isnumeric() and args.random:                     # jeśli jako ścieżka jest podany numer to wygeneruje tyle procesów
    processes = generator.rand(int(args.path), upp=args.upp) 
elif args.path.isnumeric() and args.zeroes:                   # jeśli jako ścieżka jest podany numer to wygeneruje tyle procesów
    processes = generator.zeroes(int(args.path), upp=args.upp)
elif args.path.isnumeric():
    processes = generator.normal(int(args.path), mean=args.mean, scale=args.scale, arr_up=args.upp)
else:                                                         # jeśli jest podana ścieżka to odczyta z niej procesy
    try:
        with open(args.path,'r', encoding='utf-8') as f:
            for line in f:
                processes = np.append(processes, line.split())
        processes = np.reshape(processes,(int(processes.size/2),2))
    except:
        print("Ścieżka nie wskazuje na poprawny plik!!")
        sys.exit(0)

processes = processes.astype(int)

if args.FCFS:
    schedulers.FCFS(processes)

if not args.FCFS and not args.SJF and not args.FIFO and not args.LRU and not args.LFU:
    schedulers.FCFS(processes)

if args.SJF:
    schedulers.SJF(processes)

if args.FIFO:
    processes = np.delete(processes, 0, axis=1) # do alg wymian stron przekazuje te same dane tylko bez kolumny z czasami przyjścia
    pagefile.FIFO(processes, args.frames, True)

if args.LFU:
    processes = np.delete(processes, 0, axis=1)
    pagefile.LFU(processes, args.frames, True)

if args.LRU:
    processes = np.delete(processes, 0, axis=1)
    pagefile.LRU(processes, args.frames, True)