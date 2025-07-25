import pandas as pd
import matplotlib.pyplot as plt
import panel as pn
import hvplot.pandas  # pour les graphiques interactifs
pn.extension('tabulator')

# Chargement des données
df = pd.read_csv("data/load_europe.csv", index_col=0, parse_dates=True)

# Liste des pays disponibles
countries = df.columns.tolist()

# -----------------------------
# Onglet 1 : courbe horaire simple
# -----------------------------
def plot_load(countries_selected):
    fig, ax = plt.subplots(figsize=(10, 5))
    for country in countries_selected:
        ax.plot(df.index, df[country], label=country)
    ax.set_title("Courbes de charge électriques (MW)")
    ax.set_xlabel("Heure")
    ax.set_ylabel("Puissance (MW)")
    ax.legend()
    ax.grid(True)
    return pn.pane.Matplotlib(fig, tight=True)

selector_1 = pn.widgets.MultiChoice(name='Pays', value=["France"], options=countries)
tab1 = pn.Column(
    "# Visualisation simple",
    selector_1,
    pn.bind(plot_load, countries_selected=selector_1)
)

# -----------------------------
# Onglet 2 : charge moyenne + écart-type
# -----------------------------
def compute_stats():
    stats = pd.DataFrame({
        "Moyenne (MW)": df.mean(),
        "Écart-type (MW)": df.std()
    })
    return stats.sort_values("Moyenne (MW)", ascending=False)

tab2 = pn.Column(
    "# Statistiques journalières par pays",
    pn.pane.DataFrame(compute_stats, sizing_mode='stretch_width')
)

# -----------------------------
# Onglet 3 : courbes interactives (HVPlot)
# -----------------------------
selector_3 = pn.widgets.MultiChoice(name='Pays', value=["Germany", "France"], options=countries)

def interactive_plot(pays):
    if not pays:
        return pn.pane.Markdown("Sélectionnez au moins un pays.")
    return df[pays].hvplot(title="Charge électrique interactive", xlabel="Heure", ylabel="MW")

tab3 = pn.Column(
    "# Courbe interactive (zoom possible)",
    selector_3,
    pn.bind(interactive_plot, pays=selector_3)
)

# -----------------------------
# Interface principale avec onglets
# -----------------------------
dashboard = pn.Tabs(
    ("Courbes horaires", tab1),
    ("Statistiques journalières", tab2),
    ("Plot interactif", tab3)
)

dashboard.servable()
