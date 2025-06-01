import csv, os

filename = 'window_and_lens_covered.csv'
rel_path_file = os.path.join('data\\warmup_trigger', filename)
abs_path_file = os.path.join(os.getcwd(), rel_path_file)

in_f = open(abs_path_file, 'r+')
csvReader = csv.reader(in_f, delimiter='\t')

output_filename = filename.split('.')[0] + '_formatted.csv'
rel_path_file_output = os.path.join('data\\warmup_trigger', output_filename)
abs_path_file_output = os.path.join(os.getcwd(), rel_path_file_output)

out_f = open(abs_path_file_output, 'w+', newline='')
csvWriter = csv.writer(out_f,delimiter=',')


for row in csvReader:
        print(row)
        csvWriter.writerow(row)

in_f.close()
out_f.close()