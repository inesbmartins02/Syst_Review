import csv
import sys
from collections import defaultdict

csv.field_size_limit(sys.maxsize)

def read_basta_output(file_path):
    basta_data = []
    with open(file_path, 'r') as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames 
        print("Cabeçalhos encontrados:", headers)  
        for row in reader:
            basta_data.append(row)
    return basta_data

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

def normalize_species_name(name):
    return name.replace("_", "").lower() if name else ""

def calculate_metrics(basta_data, taxonomy_mapping):
    metrics = defaultdict(lambda: {'correct': 0, 'total': 0, 'incorrect': 0, 'not_classified': 0})
    classified_gcfs = set()
    correctly_classified_gcfs = set()

    for entry in basta_data:
        gcf_id = entry['GCF_ID']
        classified_gcfs.add(gcf_id)
        if gcf_id in taxonomy_mapping:
            true_tax = taxonomy_mapping[gcf_id]
            is_correct = True
            for level in ['Kingdom', 'Phylum', 'Class', 'Order', 'Family', 'Genus', 'Species']:
                predicted_value = normalize_species_name(entry.get(level, ''))
                true_value = normalize_species_name(true_tax.get(level, ''))

                if true_value:
                    metrics[level]['total'] += 1
                    if predicted_value == true_value:
                        metrics[level]['correct'] += 1
                    else:
                        metrics[level]['incorrect'] += 1
                        is_correct = False
            if is_correct:
                correctly_classified_gcfs.add(gcf_id)
        else:
            for level in ['Kingdom', 'Phylum', 'Class', 'Order', 'Family', 'Genus', 'Species']:
                metrics[level]['total'] += 1
                metrics[level]['incorrect'] += 1

    for gcf_id in taxonomy_mapping:
        if gcf_id not in classified_gcfs:
            for level in ['Kingdom', 'Phylum', 'Class', 'Order', 'Family', 'Genus', 'Species']:
                metrics[level]['total'] += 1
                metrics[level]['incorrect'] += 1
                metrics[level]['not_classified'] += 1

    print(f"Número de GCFs classificados corretamente: {len(correctly_classified_gcfs)}")
    print(f"Número de GCFs classificados: {len(classified_gcfs)}")
    print(f"Número total de GCFs: {len(taxonomy_mapping)}")

    return metrics

def calculate_precision_recall_f1(metrics):
    results = {}
    for level, data in metrics.items():
        correct = data['correct']
        total = data['total']
        incorrect = data['incorrect']
        not_classified = data['not_classified']

        precision = correct / (correct + incorrect - not_classified) if (correct + incorrect - not_classified) > 0 else 0
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
    basta_file_path = input("Enter the path to the BASTA output transformed file (e.g., basta_output.csv): ")
    taxonomy_file_path = input("Enter the path to the taxonomy mapping file (e.g., archaea_taxonomy_mapping.csv): ")

    basta_data = read_basta_output(basta_file_path)
    taxonomy_mapping = read_taxonomy_mapping(taxonomy_file_path)

    metrics = calculate_metrics(basta_data, taxonomy_mapping)
    results = calculate_precision_recall_f1(metrics)

    print("\nTaxonomic Comparison Results:")
    for level, result in results.items():
        print(f"{level}:")
        print(f"  Precision: {result['Precision']:.2f}")
        print(f"  Recall: {result['Recall']:.2f}")
        print(f"  F1 Score: {result['F1 Score']:.2f}")
        print(f"  Not Classified: {result['Not Classified']}")

if __name__ == "__main__":
    main()
