import csv


with open('testData.csv', 'r') as test:
    with open('results.csv', 'w') as results:
        with open('test1.csv', 'r') as test1:
            reader = csv.reader(test)
            writer = csv.writer(results)
            reader1 = csv.reader(test1)

            writer.writerow(next(reader) + ['PERCENTAGE'])
            next(reader1)

            total_percent = 0
            num_loops = 0

            for row in reader:
                predicted_val = row[1]
                if num_loops < 7:
                    for row1 in reader1:
                        exact = row1[1]
                        percent_off = float(exact) / float(predicted_val)

                        total_percent = float(total_percent) + float(percent_off)

                        writer.writerow(row + [float(percent_off)])
                        break
                    num_loops = num_loops + 1

            final_percent = (total_percent / num_loops) * 100
        with open('data.txt', 'w') as data:
            if 95 <= final_percent <= 105:
                data.write("We are very confident in the prediction.\n")
            elif 85 <= final_percent <= 115:
                data.write("We are somewhat confident in the prediction.\n")
            else:
                data.write("We are not very confident in the prediction.\n")

            data.write("The stock's prediction have been {:f}% the actual value.".format(final_percent))
