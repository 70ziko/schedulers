from multiprocessing.dummy import current_process
import numpy as np

def FCFS(processes):
    sortedProc = processes[processes[:,0].argsort()]
    clock = 0 # zegar wykonywania procesu
    counter = 0 # zegar pracy procesora
    queue = np.array([], dtype=int)
    result = np.array(["Czas nadejścia", "Czas wykonywania", "Czas zakończenia", "Czas realizacji", "Czas oczekiwania"])

    # Pętla procesora
    while sortedProc.size>0 or queue.size>0:

        # Przychodzenie procesów i dodawanie ich do kolejki
        if sortedProc.size>0 and counter>=sortedProc[0][0]:
            rows = np.where(sortedProc[:,0] == sortedProc[0][0]) # szukanie procesów o takim samym czasie nadejścia
            queue = np.append(queue, sortedProc[rows])
            queue = np.reshape(queue, (int(queue.size/2), 2))
            sortedProc = np.delete(sortedProc, rows, axis=0) # zdejmowanie procesów z listy

        # Wykonywanie procesów
        if queue.size>0 and clock>=queue[0][1]: # wejdzie gdy procesor wykona proces
            result = np.append(result, [queue[0][0], queue[0][1], counter, counter-queue[0][0], counter-queue[0][0]-queue[0][1]])
            queue = np.delete(queue, 0, axis=0)
            clock = 0
        if queue.size!=0: # nie zwiększaj zegara wykonywania procesu gdy nie ma procesu do wykonywania
            clock += 1
        counter += 1

    # Wyświetlanie rezultatów i zapisywanie do pliku
    result = np.reshape(result, (int(result.size/5), 5))
    result_str = '\n'.join([''.join(['{:18}'.format(item) for item in row]) for row in result])
    result_str_file = '\n'.join([';'.join([item for item in row]) for row in result])
    result = np.delete(result, 0, axis=0) # Wywalenie opisów z tabeli

    # Liczenie i wyświetlanie średnich czasów
    avrTurnaround = (np.sum(np.asarray(result, dtype=int), axis=0)[3])/(result.size/5)
    avrWaiting = (np.sum(np.asarray(result, dtype=int), axis=0)[4])/(result.size/5)
    result_str += "\nŚredni czas realizacji: " + str(avrTurnaround)
    result_str += "\nŚredni czas oczekiwania: " + str(avrWaiting)
    result_str_file += "\nŚredni czas realizacji:;" + str(avrTurnaround)
    result_str_file += "\nŚredni czas oczekiwania:;" + str(avrWaiting)
    print(result_str)
    try:
        with open("result_FCFS.csv", 'w', encoding='utf-8') as f:
            f.write(result_str_file)
    except:
        print("Nie udało się zapisać do pliku")

def SJF(processes):
    sortedProc = processes[processes[:,0].argsort()]
    clock = 0 # zegar wykonywania procesu
    counter = 0 # zegar pracy procesora
    current = np.array([-1, -1]) # obecnie wykonywany proces
    queue = np.array([], dtype=int)
    result = np.array([])

    # Pętla procesora
    while sortedProc.size>0 or queue.size>0 :

        # Przychodzenie procesów i dodawanie ich do kolejki
        if sortedProc.size>0 and counter>=sortedProc[0][0]:
            rows = np.where(sortedProc[:,0] == sortedProc[0][0]) # szukanie procesów o takim samym czasie nadejścia
            queue = np.append(queue, sortedProc[rows])
            queue = np.reshape(queue, (int(queue.size/2), 2))
            queue = queue[queue[:,1].argsort()] # SORTOWANIE KOLEJKI WEDŁUG CZASU WYKONYWANIA
            queue = np.reshape(queue, (int(queue.size/2), 2))
            if current.size == 0 or current[1] == -1: # wybierz aktualnie wykonywany proces
                current = queue[0]
                queue = np.delete(queue,0,axis=0)
            sortedProc = np.delete(sortedProc, rows, axis=0) # zdejmowanie procesów z listy

        # Wykonywanie procesów
        if clock==current[1] or current[1] == 0: # wejdzie gdy procesor wykona proces
            result = np.append(result, [current[0], current[1], counter, counter - current[0], counter - current[0] - current[1]])
            current = queue[0]
            queue = np.delete(queue, 0, axis=0)
            clock = 0
        if current[1] != -1 and current.size != 0: # nie zwiększaj zegara wykonywania procesu gdy nie ma procesu do wykonywania
            clock += 1
        counter += 1
    result = np.append(result, [current[0], current[1], counter, counter - current[0], counter - current[0] - current[1]])
    

    # Wyświetlanie rezultatów i zapisywanie do pliku
    result = np.reshape(result, (int(result.size/5), 5))
    result = result[result[:,0].argsort()]
    result = result.astype(int)
    result = result.astype(str)

    # Liczenie i wyświetlanie średnich czasów
    avrTurnaround = (np.sum(np.asarray(result, dtype=int), axis=0)[3])/(result.size/5)
    avrWaiting = (np.sum(np.asarray(result, dtype=int), axis=0)[4])/(result.size/5)
    result_str = "Czas nadejścia    Czas wykonywania  Czas zakończenia  Czas realizacji   Czas oczekiwania\n"
    result_str_file = "Czas nadejścia;Czas wykonywania;Czas zakończenia;Czas realizacji;Czas oczekiwania\n"
    result_str += '\n'.join([''.join(['{:18}'.format(item) for item in row]) for row in result])
    result_str_file += '\n'.join([';'.join([item for item in row]) for row in result])
    result_str += "\nŚredni czas realizacji: " + str(avrTurnaround)
    result_str += "\nŚredni czas oczekiwania: " + str(avrWaiting)
    result_str_file += "\nŚredni czas realizacji:;" + str(avrTurnaround)
    result_str_file += "\nŚredni czas oczekiwania:;" + str(avrWaiting)
    print(result_str)
    try:
        with open("result_SJF.csv", 'w', encoding='utf-8') as f:
            f.write(result_str_file)
    except:
        print("Nie udało się zapisać do pliku")