import json
import os
import re
import csv

def extract_final_sequence_from_folder(folder_path, output_folder):
    pfam_files = []
    rfam_files = []
    protein_inverse_folding_files = []
    protein_structure_prediction_files = []
    rna_inverse_folding_files = []
    rna_structure_prediction_files = []

    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.json'):
                if 'Pfam_design' in file:
                    pfam_files.append(os.path.join(root, file))
                elif 'Rfam_design' in file:
                    rfam_files.append(os.path.join(root, file))
                elif 'Protein_inverse_folding' in file:
                    protein_inverse_folding_files.append(os.path.join(root, file))
                elif 'Protein_structure_prediction' in file:
                    protein_structure_prediction_files.append(os.path.join(root, file))
                elif 'RNA_inverse_folding' in file:
                    rna_inverse_folding_files.append(os.path.join(root, file))
                elif 'RNA_structure_prediction' in file:
                    rna_structure_prediction_files.append(os.path.join(root, file))

    os.makedirs(output_folder, exist_ok=True)
    pfam_output_folder = os.path.join(output_folder, 'Pfam_design')
    rfam_output_folder = os.path.join(output_folder, 'Rfam_design')
    protein_inverse_folding_output_folder = os.path.join(output_folder, 'Protein_inverse_folding')
    protein_structure_prediction_output_folder = os.path.join(output_folder, 'Protein_structure_prediction')
    rna_inverse_folding_output_folder = os.path.join(output_folder, 'RNA_inverse_folding')
    rna_structure_prediction_output_folder = os.path.join(output_folder, 'RNA_structure_prediction')
    os.makedirs(pfam_output_folder, exist_ok=True)
    os.makedirs(rfam_output_folder, exist_ok=True)
    os.makedirs(protein_inverse_folding_output_folder, exist_ok=True)
    os.makedirs(protein_structure_prediction_output_folder, exist_ok=True)
    os.makedirs(rna_inverse_folding_output_folder, exist_ok=True)
    os.makedirs(rna_structure_prediction_output_folder, exist_ok=True)

    process_files(pfam_files, pfam_output_folder, 'Pfam_design', ['0shot', '10shot'])
    process_files(rfam_files, rfam_output_folder, 'Rfam_design', ['0shot', '10shot'])
    process_files(protein_inverse_folding_files, protein_inverse_folding_output_folder, 'Protein_inverse_folding', ['0shot', '5shot'], calculate_recovery=True)
    process_files(protein_structure_prediction_files, protein_structure_prediction_output_folder, 'Protein_structure_prediction', ['0shot', '5shot'], calculate_recovery=True)
    process_files(rna_inverse_folding_files, rna_inverse_folding_output_folder, 'RNA_inverse_folding', ['0shot', '5shot'], trim_or_pad='N')
    process_files(rna_structure_prediction_files, rna_structure_prediction_output_folder, 'RNA_structure_prediction', ['0shot', '5shot'], trim_or_pad='.')

def process_files(files, output_folder, dataset_name, shot_types, calculate_recovery=False, trim_or_pad=None):
    recovery_csv_data = {}

    for file_path in files:
        model_name = os.path.basename(os.path.dirname(file_path))
        shot_type = next((shot for shot in shot_types if f'_{shot}' in file_path), None)
        if not shot_type:
            continue

        output_file_name = f"{model_name}_{dataset_name}_{shot_type}.json"
        output_file_path = os.path.join(output_folder, output_file_name)

        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        extracted_sequences = {}
        recovery_rates = {}
        for key, value in data.items():
            predictions = value.get("prediction", [])
            gold_sequence = value.get("gold", "")
            if predictions:
                last_prediction = predictions[-1].replace(" ", "")  # 移除回答中的所有空格
                if trim_or_pad == 'N':
                    sequences = re.findall(r'[A-Z]{5,}', last_prediction)
                    if sequences:
                        extracted_sequence = sequences[-1]
                        if len(extracted_sequence) < len(gold_sequence):
                            extracted_sequence = extracted_sequence.ljust(len(gold_sequence), 'N')
                        elif len(extracted_sequence) > len(gold_sequence):
                            extracted_sequence = extracted_sequence[:len(gold_sequence)]
                        extracted_sequences[key] = extracted_sequence
                    else:
                        extracted_sequences[key] = None
                elif trim_or_pad == '.':
                    dot_bracket_sequences = re.findall(r'[.()]{5,}', last_prediction)
                    if dot_bracket_sequences:
                        extracted_sequence = dot_bracket_sequences[-1]
                        if len(extracted_sequence) < len(gold_sequence):
                            extracted_sequence = extracted_sequence.ljust(len(gold_sequence), '.')
                        elif len(extracted_sequence) > len(gold_sequence):
                            extracted_sequence = extracted_sequence[:len(gold_sequence)]
                        extracted_sequences[key] = extracted_sequence
                    else:
                        extracted_sequences[key] = None
                else:
                    sequences = re.findall(r'[A-Z]{5,}', last_prediction)
                    if sequences:
                        extracted_sequence = sequences[-1]
                        if calculate_recovery:
                            if len(extracted_sequence) < len(gold_sequence):
                                extracted_sequence = extracted_sequence.ljust(len(gold_sequence), 'N')
                            elif len(extracted_sequence) > len(gold_sequence):
                                extracted_sequence = extracted_sequence[:len(gold_sequence)]
                            recovery_rate = calculate_recovery_rate(gold_sequence, extracted_sequence)
                            recovery_rates[key] = recovery_rate if recovery_rate is not None else 0.0
                        extracted_sequences[key] = extracted_sequence
                    else:
                        extracted_sequences[key] = None
                        recovery_rates[key] = 0.0 if calculate_recovery else None
            else:
                extracted_sequences[key] = None
                recovery_rates[key] = 0.0 if calculate_recovery else None

        for key, sequence in extracted_sequences.items():
            data[key]['extracted_sequence'] = sequence
            if calculate_recovery:
                data[key]['recovery_rate'] = recovery_rates[key]

        with open(output_file_path, 'w', encoding='utf-8') as output_file:
            json.dump(data, output_file, ensure_ascii=False, indent=4)

        if calculate_recovery:
            avg_recovery_rate = sum(rate for rate in recovery_rates.values() if rate is not None) / len([rate for rate in recovery_rates.values() if rate is not None]) if recovery_rates else 0
            recovery_csv_data[(model_name, dataset_name, shot_type)] = avg_recovery_rate

    if calculate_recovery and recovery_csv_data:
        csv_file_path = os.path.join(output_folder, f"{dataset_name}_recovery_rates.csv")
        with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(["Model Name", "Dataset Name", "Shot Type", "Average Recovery Rate (%)"])
            for (model_name, dataset_name, shot_type), avg_recovery_rate in recovery_csv_data.items():
                csv_writer.writerow([model_name, dataset_name, shot_type, avg_recovery_rate])

def calculate_recovery_rate(original_seq, designed_seq):
    if len(original_seq) != len(designed_seq):
        return 0.0

    matches = sum(1 for orig, desig in zip(original_seq, designed_seq) if orig == desig)
    recovery = (matches / len(original_seq)) * 100
    return recovery

folder_path = './Bio-Benchmark/inference'
output_folder = './Bio-Benchmark/extracted_sequences'
extract_final_sequence_from_folder(folder_path, output_folder)