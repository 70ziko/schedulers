import numpy as np

def index_2d(myList, v):
    for i, x in enumerate(myList):
        if v in x:
            return (i, x.index(v))

def FIFO(calls, frames, verbose):
    calls = calls.flatten() # zamienia wygenerowany array 2d na listę
    calls = calls.tolist()
    mem = [None]*frames # pamięć operacyjna o zadanej wielkości
    faults = 0
    result_str = "Lista odwołań: " + str(calls) + '\n'
    while len(calls)>0:
        result_str += "Szukam: " + str(calls[0]) + " --> "
        if calls[0] not in mem: # jeśli strona nie jest załadowana to ją wymieni
            mem.pop(0) 
            mem.append(calls[0]) 
            faults+=1
        del calls[0] 
        result_str += str(mem) + '\n'

    # Zapisywanie do pliku i na konsolę
    result_short = "Liczba wymian strony: " + str(faults)
    if verbose:
        print(result_str + result_short)
    else:
        print(result_short)
    try:
        with open("result_FIFO.txt", 'w', encoding='utf-8') as f:
            if verbose:
                f.write(result_str + result_short)
            else:
                f.write(result_short)
    except:
        print("Nie udało się zapisać do pliku")

def LFU(calls, frames, verbose):    # ZBUGOWANE TROCHĘ NIE UŻYWAĆ!!!!
    calls = calls.flatten() # zamienia wygenerowany array 2d na listę
    mem = [None]*frames # tworzy pamięć o zadanej wielkości
    faults = 0
    uses = np.array([[]], dtype=int)
    result_str = "Lista odwołań: " + str(calls) + '\n'

    while len(calls)>0:
        result_str += "Szukam: " + str(calls[0]) + " --> "
        if calls[0] not in mem:  
            if mem[0] == None:  # ładowanie do pamięci peirwszych stron
                mem = np.delete(mem,0)
            else:
                least_freq = np.where(uses == min(uses[:,1])) # zwraca tabele w uses najmniej używanych stron
                least_freq = np.delete(least_freq,1, axis=0) # wywala z tabeli wartości
                least_freq = least_freq.flatten()
                least_freq = least_freq.tolist()
                for j in least_freq:    # sprawdza czy znaleziona strona jest w pamięci
                    if uses[j][0] in mem: 
                        i = np.where(mem == uses[j][0]) # zwraca indeks w pamięci najmniej używanej strony
                        mem = np.delete(mem, i)
                        break
            mem = np.append(mem, calls[0])
            if uses.size == 0 or calls[0] not in uses[:,0]:
                uses = np.append(uses, [calls[0], 1])
                uses = np.reshape(uses, (int(uses.size/2), 2))
            faults += 1
        else:
            index = np.where(uses[:,0] == calls[0]) # znajdź miejsce ze stroną
            index = int(index[0])
            uses[index][1] += 1 # zwiększ użycie
        calls=np.delete(calls,0) # usunięcie z listy zawołań
        result_str += str(mem) + '\n'
    result_str += str(uses)

    # Zapisywanie do pliku i na konsolę
    result_short = "\nLiczba wymian strony: " + str(faults)
    if verbose: # zależnie od opcji drukuje kroki
        print(result_str + result_short)
    else:
        print(result_short)
    try:
        with open("result_LFU.txt", 'w', encoding='utf-8') as f:
            if verbose:
                f.write(result_str + result_short)
            else:
                f.write(result_short)
    except:
        print("Nie udało się zapisać do pliku")

def LRU(calls, frames, verbose):
    calls = calls.flatten() # zamienia wygenerowany array 2d na listę
    calls = calls.tolist()
    mem = [None]*frames # pamięć operacyjna o zadanej wielkości
    mem_age = mem[:]
    faults = 0
    age = 1 
    result_str = "Lista odwołań: " + str(calls) + '\n'
    while len(calls)>0:
        result_str += "Szukam: " + str(calls[0]) + " --> "
        if calls[0] not in mem: # jeśli strona nie jest załadowana to ją wymieni
            if mem[0] == None:
                mem.pop(0)
                mem_age.pop(0)
            else:
                min_value = min(mem_age, key=lambda x: x[1])[1]
                min_index = index_2d(mem_age,min_value)
                mem.pop(min_index[0]) 
                mem_age.pop(min_index[0]) 
            mem.append(calls[0])
            mem_age.append([calls[0], age]) 
            faults+=1
        else:
            for x in mem_age:
                if x is None:
                    continue
                if x[0] == calls[0]:
                    index = mem_age.index(x)
                    mem_age[index][1] = age # postarz proces
        age += 1
        del calls[0] 
        result_str += str(mem) + '\n'

    # Zapisywanie do pliku i na konsolę
    result_short = "Liczba wymian strony: " + str(faults)
    if verbose:
        print(result_str + result_short)
    else:
        print(result_short)
    with open("result_LRU.txt", 'w', encoding='utf-8') as f:
        if verbose:
            f.write(result_str + result_short)
        else:
            f.write(result_short)