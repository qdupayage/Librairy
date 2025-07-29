cost_dict = {
    'Nuclear': 47,
    'Wind': 50,
    'Hydro': 60,
    'Gas': 135,
    'Coal': 210,
    'Oil': 220,
    'Solar': 60
}
#Source	Coût_base(€/MWh)  Taxe CO2 (€/MWh)	Total estimé (€/MWh)
# Wind	      50	            0	               50
# Solar	      60	            0	               60
# Hydro       60	            0	               60
# Nuclear     45	         2(déchets)            47
# Gas	      75	      60 (0.3tCO₂/MWh)	      135
# Oil	      120	      100 (0.7tCO₂/MWh)       220
# Coal	      100	      110 (0.9tCO₂/MWh)       210