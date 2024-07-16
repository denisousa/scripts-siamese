input_file = 'clones_only_QS_EX_UD_NEW.csv'
output_file = 'filtered_clones.csv'

first_line = 'file1,start1,end1,file2,start2,end2,classification,notes\n'
text = 'apache-tomcat-7.0.2'
new_csv_list = [first_line]
for line in open(input_file, 'r').readlines():
    if text in line:
        new_csv_list.append(line)

open(output_file, 'w').write(''.join(new_csv_list))

