import requests
import concurrent.futures
import json
import logging
import time

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)

REQUESTS_PER_INTERVAL = 60
INTERVAL_DURATION = 10

def crawl_meal_by_id(meal_id):
    url = f'https://www.themealdb.com/api/json/v1/1/lookup.php?i={meal_id}'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if data.get('meals') is not None:
            return {'id': meal_id, 'data': data['meals'][0]}
        else:
            return {'id': meal_id, 'data': None}
    else:
        return {'id': meal_id, 'data': None}

def process_meal_id(meal_id):
    meal_data = crawl_meal_by_id(meal_id)
    if meal_data['data']:
        logging.info(f"Meal found for ID {meal_id}")
    else:
        logging.info(f"No meal found for ID {meal_id}")
    return meal_data

def main():
    meal_ids = range(1, 1000000)
    output_data = []

    start_time = time.time()

    with concurrent.futures.ThreadPoolExecutor() as executor:
        for meal_id in meal_ids:
            elapsed_time = time.time() - start_time
            requests_made = elapsed_time * REQUESTS_PER_INTERVAL / INTERVAL_DURATION

            if requests_made >= REQUESTS_PER_INTERVAL:
                time.sleep(INTERVAL_DURATION - elapsed_time % INTERVAL_DURATION)
                start_time = time.time()

            future = executor.submit(process_meal_id, meal_id)
            result = future.result()
            output_data.append(result)

    with open('hehe.json', 'w') as json_file:
        json.dump(output_data, json_file, indent=2)

if __name__ == "__main__":
    main()
