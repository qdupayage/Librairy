import pypsa
import pandas as pd

# Charger données horaires de consommation
df = pd.read_csv("data/load_europe.csv", index_col=0, parse_dates=True)
snapshot_hours = df.index

# Création du réseau
network = pypsa.Network()
network.set_snapshots(snapshot_hours)

# Liste de pays à modéliser (1 nœud/pays)
pays = ["Germany", "France", "Spain", "Belgium", "Netherlands"]

# Ajouter des nœuds électriques (buses) pour chaque pays
for country in pays:
    network.add("Bus", country)

    # Ajouter consommation (load) par pas horaire
    network.add("Load",
                f"load_{country}",
                bus=country,
                p_set=df[country])

    # Ajouter un générateur baseload pour équilibrer la charge (ex. nucléaire)
    network.add("Generator",
                f"nuke_{country}",
                bus=country,
                p_nom=60000,
                marginal_cost=10,
                p_max_pu=1.0)

# Ajouter lignes de transport (simplifiées)
interconnexions = [("France", "Germany"), ("France", "Spain"),
                   ("France", "Belgium"), ("Belgium", "Netherlands")]

for i, (bus1, bus2) in enumerate(interconnexions):
    network.add("Line",
                f"line_{i}",
                bus0=bus1,
                bus1=bus2,
                x=0.01,
                s_nom=20000)

# Résolution du dispatch (LP)
network.lopf()

# Export du réseau
network.export_to_netcdf("network.nc")
