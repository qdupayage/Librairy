import pandas as pd
import numpy as np

def generate_fake_energy_data(start='2023-01-01', periods=48, freq='H'):
    np.random.seed(42)
    countries = ['FR', 'DE', 'IT', 'ES']
    prod_types = ['wind', 'solar', 'nuclear', 'gas', 'coal']
    index = pd.date_range(start=start, periods=periods, freq=freq)

    data = {'DateTime': index}
    for country in countries:
        for prod in prod_types:
            data[f'prod_{prod}_{country}'] = np.random.randint(50, 500, size=len(index))

        # Demande = somme des prod ± un bruit
        prod_sum = sum(data[f'prod_{prod}_{country}'] for prod in prod_types)
        data[f'Demand_{country}'] = prod_sum + np.random.randint(-100, 100, size=len(index))

        # Prix aléatoire pour vérif visuelle
        data[f'Price_{country}'] = np.random.uniform(50, 200, size=len(index))

        # Interconnexions fictives
        for other in countries:
            if other != country:
                col = f'link_{country}_{other}'
                data[col] = np.random.randint(-50, 50, size=len(index))

    return pd.DataFrame(data)

if __name__ == '__main__':
    df = generate_fake_energy_data()
    df.to_parquet('data/fake_energy.parquet')
