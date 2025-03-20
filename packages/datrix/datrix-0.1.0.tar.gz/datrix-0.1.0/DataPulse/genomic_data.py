from faker import Faker
import pandas as pd
from flask import Flask, send_file
import random

fake = Faker()

def generate_sample_id():
    return fake.uuid4()

def generate_gene_sequence():
    return ''.join(random.choices("ATCG", k=100))

def generate_gene_name():
    return fake.bothify(text='GENE-###')

def generate_mutation_type():
    return fake.random_element(elements=["Insertion", "Deletion", "Substitution", "Duplication", "Inversion"])

def generate_chromosome_number():
    return fake.random_int(min=1, max=23)

def generate_position():
    return fake.random_int(min=1000, max=1000000)

def generate_genotype():
    return fake.random_element(elements=["AA", "AT", "TT", "CC", "GG", "AG"])

def generate_expression_level():
    return round(fake.pyfloat(left_digits=2, right_digits=3, positive=True, max_value=99.999), 3)

def generate_variation_frequency():
    return round(fake.pyfloat(left_digits=1, right_digits=5, positive=True, max_value=1.0), 5)

def generate_disease_association():
    return fake.random_element(elements=["Cancer", "Diabetes", "Alzheimer's", "Cardiovascular", "None"])

def generate_sample_source():
    return fake.random_element(elements=["Blood", "Saliva", "Tissue", "Buccal Swab"])

def generate_reference_genome():
    return fake.random_element(elements=["GRCh37", "GRCh38", "hg19", "hg38"])

def generate_gene_family():
    return fake.random_element(elements=["Kinase", "Homeobox", "Zinc Finger", "Immunoglobulin"])

def generate_transcription_factor():
    return fake.random_element(elements=["TP53", "MYC", "SOX2", "PAX6"])

def generate_snp_id():
    return fake.bothify(text='rs#####')

def generate_allele_frequency():
    return round(fake.pyfloat(left_digits=1, right_digits=6, positive=True, max_value=1.0), 6)

def generate_methylation_level():
    return round(fake.pyfloat(left_digits=2, right_digits=2, positive=True, max_value=100.0), 2)

def generate_exon_number():
    return fake.random_int(min=1, max=50)

def generate_pathogenicity_score():
    return round(fake.pyfloat(left_digits=1, right_digits=4, positive=True, max_value=1.0), 4)

def generate_genomic_data(num_records=100):
    data = [
        {
            "sample_id": generate_sample_id(),
            "gene_sequence": generate_gene_sequence(),
            "gene_name": generate_gene_name(),
            "mutation_type": generate_mutation_type(),
            "chromosome_number": generate_chromosome_number(),
            "position": generate_position(),
            "genotype": generate_genotype(),
            "expression_level": generate_expression_level(),
            "variation_frequency": generate_variation_frequency(),
            "disease_association": generate_disease_association(),
            "sample_source": generate_sample_source(),
            "reference_genome": generate_reference_genome(),
            "gene_family": generate_gene_family(),
            "transcription_factor": generate_transcription_factor(),
            "snp_id": generate_snp_id(),
            "allele_frequency": generate_allele_frequency(),
            "methylation_level": generate_methylation_level(),
            "exon_number": generate_exon_number(),
            "pathogenicity_score": generate_pathogenicity_score(),
        } for _ in range(num_records)
    ]
    return pd.DataFrame(data)

# Display sample DataFrame
df_sample = generate_genomic_data(10)
print(df_sample.head())

# # Flask app to download large datasets
# app = Flask(__name__)

# @app.route('/download_genomic_data')
# def download_genomic_data():
#     df = generate_genomic_data(500000)
#     file_path = "genomic_data.csv"
#     df.to_csv(file_path, index=False)
#     return send_file(file_path, as_attachment=True)

# if __name__ == '__main__':
#     app.run(debug=True)
