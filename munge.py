import csv

file_obj = open('data/listings.csv','r')
csv_reader = csv.DictReader(file_obj)

new_file = open ('data/listings_clean.csv', 'w', newline='')

headers = ["id","name","host_id","host_name","host_is_superhost","host_total_listings_count","host_identity_verified","neighbourhood_cleansed","room_type","accommodates",
           "beds", "price","minimum_nights_avg_ntm","maximum_nights_avg_ntm", "has_availability","number_of_reviews", "review_scores_rating"]

csv_writer = csv.DictWriter(new_file, fieldnames=headers)
csv_writer.writeheader()


for line in csv_reader:
    if  all(line[column] =='0' for column in ['availability_30','availability_60','availability_90','availability_365']):
            line['has_availability'] = 'f'

    for key, value in list(line.items()):
        if value in ['t','f']:
            line[key] = True if value == 't' else False

        elif value.isdigit() and key not in['price','review_scores_rating']:
            line[key] = int(value)

        elif key == 'price':
            try:
                clean_price = value.replace('$','').replace(',','')
                line[key] = float(clean_price)
            except: 
                line[key] = 'NaN'

        elif key == 'review_scores_rating':
            try:
                line[key] = float(value)
            except:
                line[key] = 'NaN'

        if value == '':
            line[key] = 'NaN'
            
        
    csv_writer.writerow({col: line[col] for col in headers})


file_obj.close()
new_file.close()
