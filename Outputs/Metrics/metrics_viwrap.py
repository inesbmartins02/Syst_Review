import csv
from collections import defaultdict
import sys

csv.field_size_limit(sys.maxsize)

def read_viwrap_output(file_path):
    viwrap_data = []
    with open(file_path, 'r') as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames
        print("Cabeçalhos encontrados:", headers)
        for row in reader:
            viwrap_data.append(row)
    return viwrap_data

def read_taxonomy_mapping(file_path):
    viral_taxonomy = {}
    with open(file_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            gcf_id = row['assembly_accession'].strip()
            viral_taxonomy[gcf_id] = {
                'Kingdom': row['Kingdom'].strip(),
                'Phylum': row['Phylum'].strip(),
                'Class': row['Class'].strip(),
                'Order': row.get('Order', '').strip(),
                'Family': row['Family'].strip(),
                'Genus': row['Genus'].strip(),
                'Species': row.get('Species', '').strip()
            }
    return viral_taxonomy

def calculate_metrics(viwrap_data, viral_taxonomy):
    metrics = defaultdict(lambda: {'correct': 0, 'total': 0, 'incorrect': 0, 'not_classified': 0})
    classified_gcfs = set()
    correctly_classified_gcfs = set()

    for entry in viwrap_data:
        gcf_id = entry['GCF_ID']
        classified_gcfs.add(gcf_id)
        if gcf_id in viral_taxonomy:
            true_tax = viral_taxonomy[gcf_id]
            is_correct = True
            for level in ['Kingdom', 'Phylum', 'Class', 'Order', 'Family', 'Genus', 'Species']:
                predicted_value = entry.get(level, '').strip()
                true_value = true_tax.get(level, '').strip()

                if true_value:
                    metrics[level]['total'] += 1
                    if predicted_value and predicted_value.lower() == true_value.lower():
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

    # Add unclassified GCFs as incorrect
    for gcf_id in viral_taxonomy:
        if gcf_id not in classified_gcfs:
            for level in ['Kingdom', 'Phylum', 'Class', 'Order', 'Family', 'Genus', 'Species']:
                metrics[level]['total'] += 1
                metrics[level]['incorrect'] += 1
                metrics[level]['not_classified'] += 1

    print(f"Número de GCFs classificados corretamente: {len(correctly_classified_gcfs)}")
    print(f"Número de GCFs classificados: {len(classified_gcfs)}")
    print(f"Número total de GCFs: {len(viral_taxonomy)}")

    return metrics

def calculate_precision_recall_f1(metrics):
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
    viwrap_file_path = input("Enter the path to the ViWrap output transformed file (e.g., viwrap_output.csv): ")
    taxonomy_file_path = input("Enter the path to the viral taxonomy mapping file (e.g., viral_taxonomy_mapping.csv): ")

    viwrap_data = read_viwrap_output(viwrap_file_path)
    viral_taxonomy = read_taxonomy_mapping(taxonomy_file_path)

    metrics = calculate_metrics(viwrap_data, viral_taxonomy)
    results = calculate_precision_recall_f1(metrics)

    print("\nTaxonomic Comparison Results for ViWrap:")
    for level, result in results.items():
        print(f"{level}:")
        print(f" Precision: {result['Precision']:.2f}")
        print(f" Recall: {result['Recall']:.2f}")
        print(f" F1 Score: {result['F1 Score']:.2f}")
        print(f" Not Classified: {result['Not Classified']}")

if __name__ == "__main__":
    main()
