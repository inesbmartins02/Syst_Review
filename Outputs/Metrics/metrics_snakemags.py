import csv
from collections import defaultdict
import sys

csv.field_size_limit(sys.maxsize)

def read_snakemags_output(file_path):
    snakemags_data = []
    unique_gcfs = set()
    with open(file_path, 'r') as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames 
        print("Cabeçalhos encontrados:", headers)  
        for row in reader:
            snakemags_data.append(row)
            unique_gcfs.add(row['assembly_accession'])
    return snakemags_data, unique_gcfs

def read_taxonomy_mapping(file_path):
    taxonomy_mapping = {}
    with open(file_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            gcf_id = row['assembly_accession'].strip()  
            taxonomy_mapping[gcf_id] = {
                'Kingdom': row['Kingdom'].strip(),
                'Phylum': row['Phylum'].strip(),
                'Class': row['Class'].strip(),
                'Order': row.get('Order', '').strip(),
                'Family': row['Family'].strip(),
                'Genus': row['Genus'].strip(),
                'Species': row.get('Species', '').strip()
            }
    return taxonomy_mapping

def calculate_metrics(snakemags_data, taxonomy_mapping):
    metrics = defaultdict(lambda: {'correct': 0, 'incorrect': 0, 'not_classified': 0, 'total': 0})
    classified_gcfs = set()
    correctly_classified_gcfs = set()

    for entry in snakemags_data:
        gcf_id = entry['assembly_accession']
        classified_gcfs.add(gcf_id)
        is_correct = True

        for level in ['Kingdom', 'Phylum', 'Class', 'Order', 'Family', 'Genus', 'Species']:
            predicted_value = entry.get(level, '').strip()
            true_value = taxonomy_mapping.get(gcf_id, {}).get(level, '').strip()

            metrics[level]['total'] += 1

            if predicted_value:
                if true_value and predicted_value.lower() == true_value.lower():
                    metrics[level]['correct'] += 1
                else:
                    metrics[level]['incorrect'] += 1
                    is_correct = False
            else:
                metrics[level]['not_classified'] += 1

        if is_correct:
            correctly_classified_gcfs.add(gcf_id)

    print(f"Número de GCFs classificados corretamente: {len(correctly_classified_gcfs)}")
    print(f"Número de GCFs classificados: {len(classified_gcfs)}")
    print(f"Número total de GCFs: {len(taxonomy_mapping)}")

    return metrics

def calculate_precision_recall_f1(metrics, total_gcfs):
    results = {}
    for level, data in metrics.items():
        correct = data['correct']
        total = data['total']
        incorrect = data['incorrect']
        not_classified = data['not_classified']

        precision = correct / (correct + incorrect) if (correct + incorrect) > 0 else 0
        recall = correct / total if total > 0 else 0
        f1_score = (2 * precision * recall / (precision + recall)) if (precision + recall) > 0 else 0
        
        results[level] = {
            'Precision': precision,
            'Recall': recall,
            'F1 Score': f1_score,
            'Not Classified': not_classified
        }

    return results

def main():
    snakemags_file_path = input("Enter the path to the SnakeMAGs output transformed file (e.g., snakemags_output.csv): ")
    taxonomy_file_path = input("Enter the path to the taxonomy mapping file (e.g., archaea_taxonomy_mapping.csv): ")


    snakemags_data, unique_gcfs = read_snakemags_output(snakemags_file_path)
    taxonomy_mapping = read_taxonomy_mapping(taxonomy_file_path)

    metrics = calculate_metrics(snakemags_data, taxonomy_mapping)
    results = calculate_precision_recall_f1(metrics, len(taxonomy_mapping))

    print("\nTaxonomic Comparison Results for SnakeMAGs:")
    for level, result in results.items():
        print(f"{level}:")
        print(f"  Precision: {result['Precision']:.2f}")
        print(f"  Recall: {result['Recall']:.2f}")
        print(f"  F1 Score: {result['F1 Score']:.2f}")
        print(f"  Not Classified: {result['Not Classified']}")

if __name__ == "__main__":
    main()
