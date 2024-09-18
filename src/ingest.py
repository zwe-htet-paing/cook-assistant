import os
import pandas as pd

import minsearch


DATA_PATH = os.getenv("DATA_PATH", "../data/data.csv")


def load_index(data_path=DATA_PATH):
    df = pd.read_csv(data_path)

    documents = df.to_dict(orient="records")

    index = minsearch.Index(
        text_fields=[
            'recipe_name', 
            'type_of_dish',
            'main_ingredient',
            'cuisine',
            'cooking_method',
            'prep_time',
            'cook_time',
            'instructions'
        ],
        keyword_fields=["id"],
    )

    index.fit(documents)
    return index
