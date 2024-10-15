hosty = []
with open('hosty.txt', 'r') as hosty_file:
    for line in hosty_file:
        hosty.append(line.strip())


# Tworzenie słownika hosty-narf
hosty_narf = {}
for hostname in hosty:
    narf_file = f"{hostname}-narf.txt"
    with open(narf_file, 'r') as file:
        for line in file:
            #print(line)
            if line.startswith("Gi"):
                parts = line.split("Access(VLAN ")
                #print(parts)
                if len(parts) == 2:
                    port = parts[0]
                    vlan = parts[1].split(")")[0]
                    hosty_narf[(hostname, port, vlan)] = True
                    #print("port/vlan/hosty_narf")
                    #print(port)
                    #print(vlan)
                    #print(hosty_narf)



# Tworzenie słownika hosty-sw
hosty_sw = {}
for hostname in hosty:
    sw_file = f"{hostname}-sw.txt"
    with open(sw_file, 'r') as file:
        for line in file:
            #print(line)
            if line.startswith("Gi"):
                parts = line.split()
                #print(parts)
                if len(parts) >= 4:
                    port = parts[0]
                    vlan = parts[2]
                    hosty_sw[(hostname, port, vlan)] = True
                    #print("port/vlan/hosty_sw")
                    #print(port)
                    #print(vlan)
                    #print(hosty_sw)
                   

print("Ostateczny wynik :")
print(hosty_narf)
print(hosty_sw)

# Porównywanie hosty-narf i hosty-sw
roznice = []
for host_narf in hosty_narf:
    if host_narf not in hosty_sw:
        roznice.append(f"Różnica w host-narf: {host_narf}")
        print(f"Różnica w host-narf: {host_narf}")

# Zapis wyników różnic do pliku roznice-vlan.txt z kodowaniem utf-8
with open('roznice-vlan.txt', 'w', encoding='utf-8') as roznice_file:
    for roznica in roznice:
        roznice_file.write(roznica + '\n')