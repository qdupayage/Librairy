import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def plot_timeseries(df, variables, title=None, ylabel=None, legend=True, source_type=''):
    """
    Affiche des courbes temporelles (x = DateTime).
    """
    # Vérifier la présence de DateTime
    if 'DateTime' not in df.columns:
        raise ValueError("Colonne 'DateTime' absente du DataFrame.")

    # Nettoyage : s'assurer que DateTime est bien datetime64
    df['DateTime'] = pd.to_datetime(df['DateTime'], errors='coerce')

    # Supprimer lignes vides ou incorrectes
    df = df.dropna(subset=['DateTime'])

    # Vérifie si on a des variables valides
    variables_valides = [var for var in variables if var in df.columns]
    if not variables_valides:
        raise ValueError("Aucune variable valide parmi : " + ", ".join(variables))

    # Convertir toutes les autres colonnes en numériques si besoin
    for col in df.columns:
        if col != 'DateTime':
            df[col] = pd.to_numeric(df[col], errors='coerce')

    # Affichage
    plt.figure(figsize=(15, 5))

    for var in variables_valides:
        if np.issubdtype(df[var].dtype, np.number):
            # FORCER le x explicite = DateTime
            plt.plot(df['DateTime'], df[var], label=var)
        else:
            print(f"[AVERTISSEMENT] Variable ignorée (non-numérique) : {var}")

    # Ajout titres et légendes
    if title:
        plt.title(f"{title} ({source_type.upper()})" if source_type else title)
    if ylabel:
        plt.ylabel(ylabel)

    plt.xlabel("DateTime")
    if legend:
        plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def compute_market_price_by_country(df, cost_dict):
    """
    Calcule le prix spot de l'électricité pour chaque pays selon la logique du merit order,
    en considérant les productions locales et les interconnexions.

    Parameters:
        df (pd.DataFrame): contient les colonnes de production, consommation, interconnexions, etc.
        cost_dict (dict): coûts unitaires des sources (€/MWh)

    Returns:
        pd.DataFrame: prix spot pour chaque pays, colonne par pays
        pd.DataFrame: techno marginale (celle qui fixe le prix) pour chaque heure et chaque pays
    """
    for col in df.columns:
        if col.startswith("Prod_"):
            try:
                country = col.split('_')[2]
                break
            except ValueError:
                continue
    
    # Colonnes de production pour ce pays
    prod_cols = [col for col in df.columns if col.startswith("Prod_") and col.endswith(f"_{country}")]
    # Demande
    demand_col = f"Demand_{country}"

    if demand_col not in df.columns:
        print(f"Pas de demande pour {country}, on ignore.")

    # Liste pour stocker les résultats
    price_list = []
    marginal_list = []

    for t in df.index:
        demand = pd.to_numeric(df.at[t, demand_col], errors='coerce')
        mix = []

        for col in prod_cols:
            _, tech, _ = col.split('_')
            prod_value = pd.to_numeric(df.at[t, col], errors='coerce')
            if tech in cost_dict:
                cost = cost_dict[tech]
                mix.append((cost, tech, prod_value))

        # Trier par coût croissant
        mix.sort(key=lambda x: x[0])

        reste = demand
        price = np.nan
        marginal = None

        for cost, tech, quantity in mix:
            if quantity >= reste:
                price = cost
                marginal = tech
                break
            else:
                reste -= quantity

        # Si l’offre ne suffit pas à couvrir la demande
        if np.isnan(price) and mix:
            price = mix[-1][0]
            marginal = mix[-1][1]

        price_list.append(price)
        marginal_list.append(marginal)

    # Ajouter les colonnes résultats au DataFrame
    df[f"Estimated_Price_{country}"] = price_list
    df[f"marginal_tech_{country}"] = marginal_list

    return df

def estimate_electricity_price(df, production_columns, cost_dict, demand_column):
    """
    Estime le prix moyen de l'électricité à partir des coûts de production et de la demande.

    Parameters:
        df (pd.DataFrame): contient les colonnes de production et de demande
        production_columns (list): noms des colonnes correspondant aux productions par source
        cost_dict (dict): coût unitaire de chaque source, e.g. {'nuclear': 20, 'wind': 10}
        demand_column (str): nom de la colonne de demande

    Returns:
        pd.Series: série temporelle du prix de l'électricité estimé
    """
    total_cost = pd.Series(0.0, index=df.index)
    total_production = pd.Series(0.0, index=df.index)

    for col in production_columns:
        if col in df.columns and col in cost_dict:
            total_cost += df[col] * cost_dict[col]
            total_production += df[col]

    # éviter division par zéro
    unit_price = total_cost / total_production.replace(0, np.nan)

    # Ajuster si la demande est plus grande que la production
    if demand_column in df.columns:
        supply_ratio = df[demand_column] / total_production.replace(0, np.nan)
        unit_price *= supply_ratio.clip(lower=1.0)  # surcharge si demande > production

    return unit_price.fillna(0)

#import pypsa
import pandas as pd

# def create_simple_network(df, countries, cost_dict=None):
#     """
#     Crée un réseau PyPSA à partir d'un DataFrame contenant des colonnes horodatées de production,
#     de demande et d'interconnexions entre pays.

#     Args:
#         df (pd.DataFrame): DataFrame avec index DateTime et colonnes :
#             - Demand_{country}
#             - Prod_{tech}_{country}
#             - link_{src}_{dst}
#         countries (list): liste des pays à inclure
#         cost_dict (dict): dictionnaire des coûts marginaux (€/MWh) par techno (optionnel)

#     Returns:
#         pypsa.Network
#     """
#     # 0. Prérequis
#     df = df.apply(pd.to_numeric, errors='coerce')

#     # 1. Créer le réseau
#     net = pypsa.Network()
#     net.set_snapshots(df.index)

#     # 2. Ajouter les bus
#     for country in countries:
#         net.add("Bus", name=country, country=country, carrier="AC")

#     # 3. Ajouter les charges (Load_{country})
#     for country in countries:
#         demand_col = f"Demand_{country}"
#         if demand_col in df.columns:
#             net.add("Load",
#                     name=f"Load_{country}",
#                     bus=country,
#                     p_set=df[demand_col])
#         else:
#             print(f"Avertissement : colonne {demand_col} manquante.")

#     # 4. Ajouter les générateurs (Prod_{tech}_{country})
#     for country in countries:
#         prod_cols = [col for col in df.columns if col.startswith("Prod_") and col.endswith(f"_{country}")]
#         for col in prod_cols:
#             _, tech, _ = col.split('_')
            
#             # Conversion explicite en float
#             p_max_pu = pd.to_numeric(df[col], errors='coerce')
#             p_nom = p_max_pu.max()

#             # Sécurité : ignorer si colonne vide ou sans valeurs numériques
#             if pd.isna(p_nom) or p_nom == 0:
#                 print(f"Avertissement : production vide ou nulle pour {col}, ignoré.")
#                 continue

#             net.add("Generator",
#                     name=col,
#                     bus=country,
#                     carrier=tech,
#                     p_nom=p_nom,
#                     p_max_pu=p_max_pu / p_nom,
#                     marginal_cost=cost_dict.get(tech, 100) if cost_dict else 100)

#     # 5. Ajouter les interconnexions (link_src_dst)
#     link_cols = [col for col in df.columns if col.startswith("link_")]
#     for col in link_cols:
#         try:
#             _, src, dst = col.split('_')
#         except ValueError:
#             continue

#         if src in countries and dst in countries:
#             p_set = pd.to_numeric(df[col],errors='coerce')
#             capacity = p_set.abs().max()  # approximation de capacité max
#             net.add("Link",
#                     name=col,
#                     bus0=src,
#                     bus1=dst,
#                     p_nom=capacity,
#                     p_set=p_set,
#                     marginal_cost=0,
#                     efficiency=1.0)
#         else:
#             print(f"Ignoré : {col} (src ou dst non dans {countries})")

#     return net
