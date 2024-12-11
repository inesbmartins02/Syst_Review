import csv
from collections import defaultdict
import sys

csv.field_size_limit(sys.maxsize)

def read_squeezemeta_output(file_path):
    squeezemeta_data = []
    unique_gcfs = set()

    with open(file_path, 'r') as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames
        print("Cabeçalhos encontrados:", headers)
        for row in reader:
            gcf_id = row['GCF_ID'].strip()
            if gcf_id and gcf_id not in unique_gcfs:  # Adiciona apenas GCFs únicos
                unique_gcfs.add(gcf_id)
                squeezemeta_data.append(row)

    print(f"Número de GCFs únicos lidos: {len(unique_gcfs)}")
    return squeezemeta_data, unique_gcfs

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

def calculate_metrics(squeezemeta_data, taxonomy_mapping):
    metrics = defaultdict(lambda: {'correct': 0, 'incorrect': 0, 'not_classified': 0, 'total': 0})
    classified_gcfs = set()

    for entry in squeezemeta_data:
        gcf_id = entry['GCF_ID']
        classified_gcfs.add(gcf_id)

        if gcf_id in taxonomy_mapping:
            true_tax = taxonomy_mapping[gcf_id]

            for level in ['Kingdom', 'Phylum', 'Class', 'Order', 'Family', 'Genus', 'Species']:
                predicted_value = entry.get(level, '').strip()
                true_value = true_tax.get(level, '').strip()

                metrics[level]['total'] += 1

                if predicted_value:
                    if true_value and predicted_value.lower() == true_value.lower():
                        metrics[level]['correct'] += 1
                    else:
                        metrics[level]['incorrect'] += 1
                else:
                    metrics[level]['not_classified'] += 1

    # Adicionar GCFs não classificados como incorretos
    for gcf_id in taxonomy_mapping:
        if gcf_id not in classified_gcfs:
            for level in ['Kingdom', 'Phylum', 'Class', 'Order', 'Family', 'Genus', 'Species']:
                metrics[level]['total'] += 1
                metrics[level]['incorrect'] += 1
                metrics[level]['not_classified'] += 1

    print(f"Número de GCFs classificados: {len(classified_gcfs)}")
    print(f"Número total de GCFs: {len(taxonomy_mapping)}")

    return metrics

def calculate_precision_recall_f1(metrics, total_gcfs):
    results = {}
    
    for level, data in metrics.items():
        correct = data['correct']
        total = data['total']
        incorrect = data['incorrect']
        
        precision = correct / (correct + incorrect) if (correct + incorrect) > 0 else 0
        recall = correct / total if total > 0 else 0
        f1_score = (2 * precision * recall / (precision + recall)) if (precision + recall) > 0 else 0
        
        results[level] = {
            'Precision': precision,
            'Recall': recall,
            'F1 Score': f1_score,
            'Not Classified': data['not_classified']
        }

    return results

def main():
    squeezemeta_file_path = input("Enter the path to the SqueezeMeta output transformed file (e.g., snakemags_output.csv): ")
    taxonomy_file_path = input("Enter the path to the taxonomy mapping file (e.g., archaea_taxonomy_mapping.csv): ")

    squeezemeta_data, unique_gcfs = read_squeezemeta_output(squeezemeta_file_path)
    taxonomy_mapping = read_taxonomy_mapping(taxonomy_file_path)

    metrics = calculate_metrics(squeezemeta_data, taxonomy_mapping)
    results = calculate_precision_recall_f1(metrics, len(taxonomy_mapping))

    print("\nTaxonomic Comparison Results for SqueezeMeta:")
    for level, result in results.items():
        print(f"{level}:")
        print(f" Precision: {result['Precision']:.2f}")
        print(f" Recall: {result['Recall']:.2f}")
        print(f" F1 Score: {result['F1 Score']:.2f}")
        print(f" Not Classified: {result['Not Classified']}")

if __name__ == "__main__":
    main()
