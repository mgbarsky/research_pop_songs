from count_utils import *
from tfidf_utils import *

if __name__=='__main__':
    doc_term_2D_array = create_tfidf_input_for_clustering()
    with open('clustering/tfidf_cluster_input.tsv', 'w') as output:
        for item in doc_term_2D_array:
            row = ''
            for i in range(len(item)-1):
                row = row + str(item[i]) + '\t'
            row = row + str(item[-1]) + '\n'
            output.write(row)


    sorted_word_dict, country_fre_all = create_count_input_for_clustering()
    with open('clustering/count_cluster_input.tsv', 'w') as csv_file:
        csv_file.write('\t'.join(sorted_word_dict.keys()) + '\n')
        for key in country_fre_all.keys():
            row = ''
            for value in country_fre_all[key]:
                row = row + '\t' + str(value)
            row = key + row + '\n'
            csv_file.write(row)
