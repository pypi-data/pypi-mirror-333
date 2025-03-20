# List the example data files.
EXAMPLE_FILES = {
    "file1": "./example_data/vcf_files/testing_vcf.vcf",
    "file2": "./example_data/vcf_files/testing_vcf2.vcf"
}

# List of relevant paths.
PATH_TO_DEEP_PILEUP_REPOSITORY = "/Users/nicholasabad/Desktop/workspace/data/deep_pileup/pcawg"
PATH_TO_GENOME_TORNADO_PLOTS_REPOSITORY = "./example_data/tornado_plots"

# Set the required columns
REQUIRED_COLUMNS = [
    'score',
    'pid',
    'cohort',
    '#CHROM',
    'POS',
    'GENE',
    'REF',
    'ALT',
    'strand',
    'FPKM',
    'FPKM_Z_score',
    'cn_score',
    'ICGC_Estimated_Purity',
    'num_paths_of_recurrence',
    'within_cgc_list',
    'within_chromhmm_promoter',
    'allele_frequency',
    'JASPAR2020_CORE_vertebrates_non_redundant(tf_name,binding_affinity,seq1,seq2,raw,zscore,log)',
    'paths_with_recurrence(format=path,pid,cohort,bp,ref,alt,gene,chr,raw_score,zscore,log_score,confidence,purity,af,(tfs_seperated_by_//))',
    'number_of_pcawg_recurrent_mutations',
    'path_to_pcawg_recurrence_dict',
    'JASPAR2020_CORE_vertebrates_non_redundant(tf_name,binding_affinity,seq1,seq2,raw,zscore,log,tf_sequence_logo)',
    'num_original_mutations',
    'num_final_mutations',
    'num_promoter_mutations',
    'num_recurrent_mutations',
    'expression_traces',
    'cn_file_of_score',
]

DATAFRAME_SETTINGS = {
    "name_of_the_gene_column": "GENE",
    "name_of_the_chromosome_column": "#CHROM",
    "name_of_reference_nucleotide_column": "REF",
    "name_of_alternative_nucleotide_column": "ALT",
    "name_of_position_column": "POS",
    "name_of_sequence_context_column": "SEQUENCE_CONTEXT",
    "name_of_expression_column": "FPKM",
    "name_of_normalized_expression_column": "FPKM_Z_score",
    
    "name_of_cohort_column": "cohort",
    
    "name_of_column_with_list_of_created_tfbs": "created_tfs_passing_tf_expression_threshold",
    "name_of_column_with_list_of_destroyed_tfbs": "destroyed_tfs_passing_tf_expression_threshold",
    
    "name_of_tfbs_column": "JASPAR2020_CORE_vertebrates_non_redundant(tf_name,binding_affinity,seq1,seq2,raw,zscore,log,tf_sequence_logo)",
    "tfbs_binding_affinity_creation_threshold": 11,
    "tfbs_binding_affinity_destruction_threshold": 0.09,
    
    "name_of_paths_with_recurrence_column": "paths_with_recurrence(format=path,pid,cohort,bp,ref,alt,gene,chr,raw_score,zscore,log_score,confidence,purity,af,(tfs_seperated_by_//))",
    
    "name_of_expression_traces_column": "expression_traces",
    "name_of_pid_column": "pid"
}

DATAFRAME_SETTING_DESCRIPTION = {
    "name_of_the_gene_column": {
        "description": "Name of the column within the .vcf file that denotes the name of the gene.",
        "datatype_of_data_within_column": "str",
        "example_of_data_within_column": "TERT"
    },
    "name_of_the_chromosome_column": {
        "description": "Name of the chromosome column (without chr)",
        "datatype_of_data_within_column": "str",
        "example_of_data_within_column": "7"
    },
    "name_of_reference_nucleotide_column": {
        "description": "Name of the column that denotes the reference nucleotide",
        "datatype_of_data_within_column": "str",
        "example_of_data_within_column": "A"
    },
    "name_of_reference_nucleotide_column": {
        "description": "Name of the column that denotes the alternative nucleotide",
        "datatype_of_data_within_column": "str",
        "example_of_data_within_column": "T"
    },
    "name_of_column_with_list_of_created_tfbs": {
        "description": "Name of the column with all of the created TFs introduced by a mutation.",
        "datatype_of_data_within_column": "column name is a string whereas the contents are strings separated by a comma",
        "example_of_data_within_column": "'ZBTB7A','ELK4'" 
    },
    "name_of_column_with_list_of_destroyed_tfbs": {
        "description": "Name of the column with all of the destroyed TFs introduced by a mutation.",
        "datatype_of_data_within_column": "column name is a string whereas the contents are strings separated by a comma",
        "example_of_data_within_column": "'ZBTB7A','ELK4'" 
    },
    "name_of_tf_column": {
        "description": "Name of the column with all details of the created/destroyed TFBSs introduced by the mutation. This was created within the REMIND-Cancer pipeline.",
        "datatype_of_data_within_column": "str",
        "example_of_data_within_column": "REL,13.2727,.,GGGAGTTTCC,0.298502304678,-1.254585723945777,-1.2089776253149644,https://jaspar.genereg.net/static/logos/all/MA0101.1.png;NFKB1,1.8009713394286062,AGGGAGTCTCCCT,AGGGAGTTTCCCT,5.19415624061,-1.300156076846545,1.64753419376811,https://jaspar.genereg.net/static/logos/all/MA0105.4.png;RELA,16.2959,.,GGGAGTTTCC,22.0994861,0.1817001390484236,3.0955543548596776,https://jaspar.genereg.net/static/logos/all/MA0107.1.png;STAT1,16.0455,.,GGAGTTTCCCTTTCC,19.0316786755,-0.6927473462662653,2.9461048894775086,https://jaspar.genereg.net/static/logos/all/MA0137.3.png;STAT2,16.0455,.,GGAGTTTCCCTTTCC,11.9365407518,-1.1933806103644888,2.4796043467079856,not_available;NFKB2,1.2807036165039176,AGGGAGACTCCCT,AGGGAGTTTCCCT,15.0812879602,-0.2587310828247882,2.7134547674340377,https://jaspar.genereg.net/static/logos/all/MA0778.1.png",
        "extra_details": [
            "Since there could be multiple TFBS affected by the mutation, each newly created/destroyed TFBS _entry_ is separated by the ';' delimiter.",
            "Each _subentry_ in a singular TFBS _entry_ is separated by the delimiter ','.",
            "Each _subentry_ has the following format: (tf_name,binding_affinity,seq1,seq2,raw,zscore,log,tf_sequence_logo)",
            "For example, take the first entry of example_of_data_within_column above: REL,13.2727,.,GGGAGTTTCC,0.298502304678,-1.254585723945777,-1.2089776253149644,https://jaspar.genereg.net/static/logos/all/MA0101.1.png",
            "REL is tf_name, 13.2727 is the binding_affinity, seq1 is ., seq2 is GGGAGTTTCC, etc."
        ]
    }
}