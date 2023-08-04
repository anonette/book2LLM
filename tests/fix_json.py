
import os, json
def standardize_json(file_path, output_file_path):
    with open(file_path, "r") as f:
        data = json.load(f)

    # Iterate over data and standardize the structure of 'questions'
    for title_block in data:
        if 'paragraphs' in title_block:
            for paragraph in title_block['paragraphs']:
                if 'questions' in paragraph:
                    standardized_questions = []
                    for question in paragraph['questions']:
                        if isinstance(question, dict):
                            standardized_questions.append(question)
                        else:  # assuming it's a string
                            standardized_questions.append({"question": question})
                    # Replace the 'questions' list with the standardized one
                    paragraph['questions'] = standardized_questions

    # Write the standardized data to a new JSON file
    with open(output_file_path, "w") as f:
        json.dump(data, f, indent=4)

standardize_json("C:\\dev\\book2LLM\\data\\merged.json", "C:\\dev\\book2LLM\\data\\merged_fix.json")