# Cooking Assistant - A Recipe RAG Application

## Problem Description

Many people find it difficult to get personalized and easy-to-use cooking help. Most platforms are either too complicated or don’t offer enough customization.

Cooking Assistant solves this problem by using a RAG-powered model to provide recipe recommendations, ingredient substitutions, and step-by-step instructions from a dataset of 182 recipes. It offers a simple, interactive solution that makes cooking easier and more efficient.

## Project Overview
Cooking Assistant is a RAG application designed to assist users with their cooking needs.

The main use cases include:

1. **Recipe Selection**: Recommending recipes based on dish type, cuisine, or main ingredients.
2. **Recipe Replacement**: Suggesting alternative recipes or ingredient substitutions.
3. **Cooking Instructions**: Providing step-by-step guidance on how to prepare a dish.
4. **Conversational Interaction**: Offering easy access to recipe information without browsing through websites or cookbooks.
This application simplifies meal preparation by delivering personalized cooking assistance in real-time.

## Dataset

The dataset used in this project was generated using ChatGPT and contains 182 recipe records. It provides comprehensive details about various dishes and is structured in the following format:

| Column Name       | Description                                                                                 |
|-------------------|---------------------------------------------------------------------------------------------|
| `recipe_name`      | The name of the recipe (e.g., *Spaghetti Bolognese*)                                        |
| `type_of_dish`     | The category of the dish (e.g., *Main Course*)                                              |
| `main_ingredient`  | The primary ingredient used in the recipe (e.g., *Beef*)                                    |
| `cuisine`          | The cuisine type of the recipe (e.g., *Italian*)                                            |
| `cooking_method`   | The method used to cook the dish (e.g., *Simmering*)                                        |
| `prep_time`        | The preparation time required (e.g., *10 minutes*)                                          |
| `cook_time`        | The time it takes to cook the dish (e.g., *40 minutes*)                                     |
| `instructions`     | Detailed step-by-step instructions for preparing the dish                                   |

Example of a recipe entry:

```plaintext
recipe_name: Spaghetti Bolognese
type_of_dish: Main Course
main_ingredient: Beef
cuisine: Italian
cooking_method: Simmering
prep_time: 10 minutes
cook_time: 40 minutes
instructions: Heat olive oil in a large pan over medium heat. Add finely chopped onions, carrots, and celery. Cook for 5-7 minutes until softened. Add minced beef and cook until browned. Pour in canned tomatoes, beef broth, and Italian herbs. Simmer uncovered for 30-40 minutes. Stir occasionally and season with salt and pepper. Serve over cooked spaghetti and garnish with fresh basil.
```

## Technoligies

* [Minisearch](https://github.com/alexeygrigorev/minisearch) - for full-text-search
* OpenAI as an LLM
* Flask as the API interface (see [Background](#background)) - for more info

## Running it with Docker

The easiest way to run this application is with docker:

```bash
docker-compose up
```

If you need to change something in the dockerfile and test it quickly, you can use the following commands:

```bash
docker build -t cooking-assistant .
```

```bash
docker run -it --rm \
    --network="llm-rag-project_default" \
    --env-file=".env" \
    -e OPENAI_API_KEY=${OPENAI_API_KEY} \
    -e DATA_PATH="data/data.csv" \
    -p 5000:5000 \
    cooking-assistant
```

## Running locally
### Installing the dependencies

If you don't use docker and want to run locally, you need to manually prepare the environment and install all the dependencies.

We use `pipenv` for managing dependencies and Python 3.12.

Make sure you have pipenv installed:

```bash
pipenv install --dev
```

### Running the application

For running the application locally, do this:

```bash
pipenv run python app.py
```

## Preparing the applicaton

Before we can use the app, we need to initialize the database.

We can do it by running the [`db_prep.py`](src/db_prep.py) script;

```bash
pipenv run python db_prep.py
```

## Using the application

First, you need to start the application either with docker-compose or locally.

When it's running, let's test it:

```bash
URL=http://localhost:5000
QUESTION="What should I do after cooking the onions, carrots, and celery?"
DATA='{
    "question": "'${QUESTION}'"
}'

curl -X POST \
    -H "Content-Type: application/json" \
    -d "${DATA}" \
    ${URL}/question
```

You will see something like the following in the response:

```json
{'answer': 'After pouring the filling over the crust for the Lemon Bars, you should bake them until set, which typically takes about 30 minutes.', 'conversation_id': '9b99ab97-ddd4-4bf7-b759-7b1b1a9b93bc', 'question': 'After pouring the filling over the crust, how long should I bake the bars until they are set?'}
```

Sending feedback:

```bash
ID="62a747fd-d748-4d1c-813f-4575ab4e8d96"
URL=http://localhost:5000
FEEDBACK_DATA='{
    "conversation_id": "'${ID}'",
    "feedback": 1
}'

curl -X POST \
    -H "Content-Type: application/json" \
    -d "${FEEDBACK_DATA}" \
    ${URL}/feedback
```

After sending it, you'll receive the acknowledgement:

```json
{
  "message": "Feedback received for conversation 62a747fd-d748-4d1c-813f-4575ab4e8d96: 1"
}
```

Alternatively, you can use [test.py](test.py) for testing it:

```bash
pipenv run python test.py
```

### Misc

Running jupyter notebook for experiments:

```bash
cd notebooks
pipenv run jupyter notebook
```

## Interface

We use Flask for serving the application as API.

Refer to ["Running the Application" section](#running-the-application) for more detail.


## Ingestion

The ingestion script is in [src/ingest.py](src/ingest.py) and it's run on the startup of the app (in [src/rag.py](src/rag.py))

## Evaluation

For the code for evaluating the system, you can check the [notebooks/rag-test.ipynb](notebooks/rag-test.ipynb) notebook.

We generated the ground truth dataset using this notebook: [notebooks/evaluation-data-generation.ipynb](notebooks/evaluation-data-generation.ipynb)

## Retrieval

The basic approach - using minisearch without any boosting - gave the following metrics:

* hit_rate: 86%
* MRR: 71%

The improved version (with better boosting):

* hit_rate: 87%
* MRR: 74%

The best boosting parameters:
```python
boost = {
    'exercise_name': 2.31984897428916,
    'type_of_activity': 1.4242161164765066,
    'type_of_equipment': 0.8557405139948276,
    'body_part': 0.1592615373833831,
    'type': 1.7674132568449183,
    'muscle_groups_activated': 2.8318029512403116,
    'instructions': 0.018866767130518602
    }
```


## RAG flow

We used the LLM-as-a-Judge metric to evaluate the quality of our RAG flow

For gtp-4o-mini, among 910 records, we had:

* 807 (88%) RELEVANT
* 91 (10%) PARTLY_RELEVANT
* 12 (1%) IRRELEVANT

## Monitoring