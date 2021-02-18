import csv


def load_tasks_data_from_csv(file_path: str):
    tasks_data = []

    with open(file_path) as csvfile:
        reader = csv.reader(csvfile)
        headers = next(reader, None)
        assert type(headers) is list and len(headers) > 0

        for row in reader:
            data = {}
            for i in range(len(headers)):
                data[headers[i]] = row[i]
            tasks_data.append(data)

    return tasks_data
