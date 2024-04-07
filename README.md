# AirBnB MongoDB Analysis

I am working with [AirBnB data](https://insideairbnb.com/get-the-data/) from Singapore, Singapore originally in CSV format. Download the original data set [here](https://data.insideairbnb.com/singapore/sg/singapore/2023-12-26/data/listings.csv.gz). I chose to clean the dataset for this workshop.

Below are the first 10 rows:
| id | name | host_id | host_name | host_is_superhost | host_total_listings_count | host_identity_verified | neighbourhood_cleansed | room_type | accommodates | beds | price | minimum_nights_avg_ntm | maximum_nights_avg_ntm | has_availability | number_of_reviews | review_scores_rating |
|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|
| 71609 | Villa in Singapore · ★4.44 · 2 bedrooms · 3 beds · 1 private bath | 367042 | Belinda | False | 15 | True | Tampines | Private room | 3 | 3 | 150.0 | 92.0 | 1125.0 | True | 19 | 4.44 |
| 71896 | Home in Singapore · ★4.16 · 1 bedroom · 1 bed · Shared half-bath | 367042 | Belinda | False | 15 | True | Tampines | Private room | 1 | 1 | 80.0 | 92.0 | 1125.0 | True | 24 | 4.16 |
| 71903 | Home in Singapore · ★4.41 · 1 bedroom · 2 beds · Shared half-bath | 367042 | Belinda | False | 15 | True | Tampines | Private room | 2 | 2 | 80.0 | 92.0 | 1125.0 | True | 46 | 4.41 |
| 275343 | Rental unit in Singapore · ★4.40 · 1 bedroom · 1 bed · 2 shared baths | 1439258 | Kay | False | 68 | True | Bukit Merah | Private room | 1 | 1 | 64.0 | 60.0 | 1125.0 | True | 20 | 4.4 |
| 275344 | Rental unit in Singapore · ★4.27 · 1 bedroom · 1 bed · 2.5 shared baths | 1439258 | Kay | False | 68 | True | Bukit Merah | Private room | 1 | 1 | 78.0 | 60.0 | 1125.0 | True | 16 | 4.27 |
| 289234 | Home in Singapore · ★4.83 · 3 bedrooms · 5 beds · 3 baths | 367042 | Belinda | False | 15 | True | Tampines | Private room | 4 | 5 | 220.0 | 92.0 | 1125.0 | True | 12 | 4.83 |
| 294281 | Rental unit in Singapore · ★4.43 · 2 bedrooms · 1 bed · 1 shared bath | 1521514 | Elizabeth | False | 8 | True | Newton | Private room | 2 | 1 | 85.0 | 92.0 | 1125.0 | True | 131 | 4.43 |
| 324945 | Rental unit in Singapore · ★3.50 · 1 bedroom · 1 bed · 2 shared baths | 1439258 | Kay | False | 68 | True | Bukit Merah | Private room | 1 | 1 | 75.0 | 60.0 | 1125.0 | True | 17 | 3.5 |
| 330095 | Rental unit in Singapore · ★3.80 · 1 bedroom · 1 bed · 2 shared baths | 1439258 | Kay | False | 68 | True | Bukit Merah | Private room | 1 | 1 | 69.0 | 60.0 | 1125.0 | True | 5 | 3.8 |


### Data scrubbing
In `munge.py`, I cleaned my dataset by removing all columns with no values, so columns description, `neighborhood`, `bathrooms`, `amenities`, `calendar_updated`, and `bedrooms`. I also removed the `license` column since more than 3/4 of the dataset had missing values. 

To deal with other missing values throughout the dataset, I replaced them with `NaN`.

Lastly, I noticed that several listings had 0 availability under all of the availability columns but still had the `has_availability` field marked as `t`, which demostrates logical issues. So, I decided to change the `has_availability` field to `f` for all listings that had `0` value for all their availability columns (`availability_30`, `availability_60`...).

### MongoDB import
With my clean CSV file ready, I then uploaded it to my database using Cyberduck. Below is the command used to import the dataset: 

```
mongoimport --headerline --type csv --db dt2211 --collection listings1 --host class-mongodb.cims.nyu.edu --file listings_clean.csv --username dt2211 --password (...)
 ```

### Data Analysis 
```
module load mongodb-4.0
mongosh dt2211 --host class-mongodb.cims.nyu.edu -u dt2211 -p
```

1. show exactly two documents from the `listings` collection in any order
Query:
```
db.listings.find().limit(2)
```
Result:
```
[
  {
    _id: ObjectId('6611c6e8c34b7fbd6a5aa97b'),
    id: 275343,
    name: 'Rental unit in Singapore · ★4.40 · 1 bedroom · 1 bed · 2 shared baths',
    host_id: 1439258,
    host_name: 'Kay',
    host_is_superhost: 'False',
    host_total_listings_count: 68,
    host_identity_verified: 'True',
    neighbourhood_cleansed: 'Bukit Merah',
    room_type: 'Private room',
    accommodates: 1,
    beds: 1,
    price: 64,
    minimum_nights_avg_ntm: 60,
    maximum_nights_avg_ntm: 1125,
    has_availability: 'True',
    number_of_reviews: 20,
    review_scores_rating: 4.4
  },
  {
    _id: ObjectId('6611c6e8c34b7fbd6a5aa97c'),
    id: 275344,
    name: 'Rental unit in Singapore · ★4.27 · 1 bedroom · 1 bed · 2.5 shared baths',
    host_id: 1439258,
    host_name: 'Kay',
    host_is_superhost: 'False',
    host_total_listings_count: 68,
    host_identity_verified: 'True',
    neighbourhood_cleansed: 'Bukit Merah',
    room_type: 'Private room',
    accommodates: 1,
    beds: 1,
    price: 78,
    minimum_nights_avg_ntm: 60,
    maximum_nights_avg_ntm: 1125,
    has_availability: 'True',
    number_of_reviews: 16,
    review_scores_rating: 4.27
  }
]
```
Insights: 
- This query outputs the first two documents from the listings1 collection, providing a snapshot of Singapore properties. 

2. show exactly 10 documents in any order, but "prettyprint" in easier to read format, using the `pretty()` function.
Query:
```
db.listings1.find().limit(10).pretty()
```
Results:
```
[
  {
    _id: ObjectId('6611c6e8c34b7fbd6a5aa97b'),
    id: 275343,
    name: 'Rental unit in Singapore · ★4.40 · 1 bedroom · 1 bed · 2 shared baths',
    host_id: 1439258,
    host_name: 'Kay',
    host_is_superhost: 'False',
    host_total_listings_count: 68,
    host_identity_verified: 'True',
    neighbourhood_cleansed: 'Bukit Merah',
    room_type: 'Private room',
    accommodates: 1,
    beds: 1,
    price: 64,
    minimum_nights_avg_ntm: 60,
    maximum_nights_avg_ntm: 1125,
    has_availability: 'True',
    number_of_reviews: 20,
    review_scores_rating: 4.4
  },
  {
    _id: ObjectId('6611c6e8c34b7fbd6a5aa97c'),
    id: 275344,
    name: 'Rental unit in Singapore · ★4.27 · 1 bedroom · 1 bed · 2.5 shared baths',
    host_id: 1439258,
    host_name: 'Kay',
    host_is_superhost: 'False',
    host_total_listings_count: 68,
    host_identity_verified: 'True',
    neighbourhood_cleansed: 'Bukit Merah',
    room_type: 'Private room',
    accommodates: 1,
    beds: 1,
    price: 78,
    minimum_nights_avg_ntm: 60,
    maximum_nights_avg_ntm: 1125,
    has_availability: 'True',
    number_of_reviews: 16,
    review_scores_rating: 4.27
  },
  {
    _id: ObjectId('6611c6e8c34b7fbd6a5aa97d'),
    id: 289234,
    name: 'Home in Singapore · ★4.83 · 3 bedrooms · 5 beds · 3 baths',
    host_id: 367042,
    host_name: 'Belinda',
    host_is_superhost: 'False',
    host_total_listings_count: 15,
    host_identity_verified: 'True',
    neighbourhood_cleansed: 'Tampines',
    room_type: 'Private room',
    accommodates: 4,
    beds: 5,
    price: 220,
    minimum_nights_avg_ntm: 92,
    maximum_nights_avg_ntm: 1125,
    has_availability: 'True',
    number_of_reviews: 12,
    review_scores_rating: 4.83
  },
  {
    _id: ObjectId('6611c6e8c34b7fbd6a5aa97e'),
    id: 294281,
    name: 'Rental unit in Singapore · ★4.43 · 2 bedrooms · 1 bed · 1 shared bath',
    host_id: 1521514,
    host_name: 'Elizabeth',
    host_is_superhost: 'False',
    host_total_listings_count: 8,
    host_identity_verified: 'True',
    neighbourhood_cleansed: 'Newton',
    room_type: 'Private room',
    accommodates: 2,
    beds: 1,
    price: 85,
    minimum_nights_avg_ntm: 92,
    maximum_nights_avg_ntm: 1125,
    has_availability: 'True',
    number_of_reviews: 131,
    review_scores_rating: 4.43
  },
  {
    _id: ObjectId('6611c6e8c34b7fbd6a5aa97f'),
    id: 324945,
    name: 'Rental unit in Singapore · ★3.50 · 1 bedroom · 1 bed · 2 shared baths',
    host_id: 1439258,
    host_name: 'Kay',
    host_is_superhost: 'False',
    host_total_listings_count: 68,
    host_identity_verified: 'True',
    neighbourhood_cleansed: 'Bukit Merah',
    room_type: 'Private room',
    accommodates: 1,
    beds: 1,
    price: 75,
    minimum_nights_avg_ntm: 60,
    maximum_nights_avg_ntm: 1125,
    has_availability: 'True',
    number_of_reviews: 17,
    review_scores_rating: 3.5
  },
  {
    _id: ObjectId('6611c6e8c34b7fbd6a5aa980'),
    id: 330095,
    name: 'Rental unit in Singapore · ★3.80 · 1 bedroom · 1 bed · 2 shared baths',
    host_id: 1439258,
    host_name: 'Kay',
    host_is_superhost: 'False',
    host_total_listings_count: 68,
    host_identity_verified: 'True',
    neighbourhood_cleansed: 'Bukit Merah',
    room_type: 'Private room',
    accommodates: 1,
    beds: 1,
    price: 69,
    minimum_nights_avg_ntm: 60,
    maximum_nights_avg_ntm: 1125,
    has_availability: 'True',
    number_of_reviews: 5,
    review_scores_rating: 3.8
  },
  {
    _id: ObjectId('6611c6e8c34b7fbd6a5aa981'),
    id: 369141,
    name: 'Place to stay in Singapore · ★4.43 · 1 bedroom · 1 bed · 1 bath',
    host_id: 1521514,
    host_name: 'Elizabeth',
    host_is_superhost: 'False',
    host_total_listings_count: 8,
    host_identity_verified: 'True',
    neighbourhood_cleansed: 'Newton',
    room_type: 'Private room',
    accommodates: 2,
    beds: 1,
    price: 79,
    minimum_nights_avg_ntm: 92,
    maximum_nights_avg_ntm: 180,
    has_availability: 'True',
    number_of_reviews: 81,
    review_scores_rating: 4.43
  },
  {
    _id: ObjectId('6611c6e8c34b7fbd6a5aa982'),
    id: 369145,
    name: 'Townhouse in Singapore · ★4.39 · 2 bedrooms · 1 bed · 1 shared bath',
    host_id: 1521514,
    host_name: 'Elizabeth',
    host_is_superhost: 'False',
    host_total_listings_count: 8,
    host_identity_verified: 'True',
    neighbourhood_cleansed: 'Newton',
    room_type: 'Private room',
    accommodates: 2,
    beds: 1,
    price: 70,
    minimum_nights_avg_ntm: 92,
    maximum_nights_avg_ntm: 1125,
    has_availability: 'True',
    number_of_reviews: 163,
    review_scores_rating: 4.39
  },
  {
    _id: ObjectId('6611c6e8c34b7fbd6a5aa983'),
    id: 395191,
    name: 'Rental unit in Singapore · ★4.31 · 1 bedroom · 1 bed · 0 baths',
    host_id: 1975201,
    host_name: 'Adi',
    host_is_superhost: 'False',
    host_total_listings_count: 2,
    host_identity_verified: 'True',
    neighbourhood_cleansed: 'River Valley',
    room_type: 'Private room',
    accommodates: 1,
    beds: 1,
    price: 100,
    minimum_nights_avg_ntm: 93,
    maximum_nights_avg_ntm: 365,
    has_availability: 'True',
    number_of_reviews: 27,
    review_scores_rating: 4.31
  },
  {
    _id: ObjectId('6611c6e8c34b7fbd6a5aa984'),
    id: 468782,
    name: 'Home in Singapore · ★4.69 · 1 bedroom · 1.5 baths',
    host_id: 2327208,
    host_name: 'Jerome',
    host_is_superhost: 'False',
    host_total_listings_count: 3,
    host_identity_verified: 'True',
    neighbourhood_cleansed: 'Serangoon',
    room_type: 'Private room',
    accommodates: 2,
    beds: NaN,
    price: 60,
    minimum_nights_avg_ntm: 92,
    maximum_nights_avg_ntm: 180,
    has_availability: 'True',
    number_of_reviews: 82,
    review_scores_rating: 4.69
  }
]
```
Insights: 
- Pretty printing makes it easier to read the output. 


3. choose two hosts (by reffering to their `host_id` values) who are superhosts (available in the `host_is_superhost` field), and show all of the listings offered by both of the two hosts
   - only show the `name`, `price`, `neighbourhood`, `host_name`, and `host_is_superhost` for each result
Query:
```
   db.listings1.find({$or: [{host_id: 11390076}, {host_id: 23336011}]}, {_id: 0, name: 1, price:1, neighbourhood_cleansed:1, host_name:1, host_is_superhost:1})
```
Result:
```
[
  {
    name: 'Aparthotel in Singapore · ★4.81 · Studio · 1 bed · 1 bath',
    host_name: 'Heritage',
    host_is_superhost: 'True',
    neighbourhood_cleansed: 'Downtown Core',
    price: 203
  },
  {
    name: 'Rental unit in Singapore · ★4.29 · 1 bedroom · 1 bed · 2 shared baths',
    host_name: 'Tryston',
    host_is_superhost: 'True',
    neighbourhood_cleansed: 'Toa Payoh',
    price: 80
  },
  {
    name: 'Aparthotel in Singapore · ★4.77 · Studio · 1 bed · 1 bath',
    host_name: 'Heritage',
    host_is_superhost: 'True',
    neighbourhood_cleansed: 'Singapore River',
    price: 198
  },
  {
    name: 'Aparthotel in Singapore · ★4.70 · Studio · 1 bed · 1 bath',
    host_name: 'Heritage',
    host_is_superhost: 'True',
    neighbourhood_cleansed: 'Downtown Core',
    price: 188
  },
  {
    name: 'Aparthotel in Singapore · ★4.67 · 1 bedroom · 1 bed · 1 bath',
    host_name: 'Heritage',
    host_is_superhost: 'True',
    neighbourhood_cleansed: 'Downtown Core',
    price: 179
  },
  {
    name: 'Rental unit in Singapore · ★4.0 · 1 bedroom · 1 bed · 1 private bath',
    host_name: 'Tryston',
    host_is_superhost: 'True',
    neighbourhood_cleansed: 'Museum',
    price: 75
  },
  {
    name: 'Aparthotel in Singapore · ★4.78 · 1 bedroom · 1 bed · 1 bath',
    host_name: 'Heritage',
    host_is_superhost: 'True',
    neighbourhood_cleansed: 'Outram',
    price: 135
  },
  {
    name: 'Rental unit in Singapore · ★5.0 · 1 bedroom · 1 bed · 2 shared baths',
    host_name: 'Tryston',
    host_is_superhost: 'True',
    neighbourhood_cleansed: 'Toa Payoh',
    price: 58
  },
  {
    name: 'Aparthotel in Singapore · ★4.79 · 1 bedroom · 1 bed · 1 bath',
    host_name: 'Heritage',
    host_is_superhost: 'True',
    neighbourhood_cleansed: 'Outram',
    price: 159
  },
  {
    name: 'Rental unit in Singapore · ★5.0 · 1 bedroom · 1 bed · 1 bath',
    host_name: 'Heritage',
    host_is_superhost: 'True',
    neighbourhood_cleansed: 'Outram',
    price: 135
  },
  {
    name: 'Rental unit in Singapore · ★5.0 · 1 bedroom · 1 bed · 1 bath',
    host_name: 'Heritage',
    host_is_superhost: 'True',
    neighbourhood_cleansed: 'Outram',
    price: 153
  },
  {
    name: 'Condo in Singapore · ★4.0 · 1 bedroom · 1 bed · 2 shared baths',
    host_name: 'Tryston',
    host_is_superhost: 'True',
    neighbourhood_cleansed: 'Toa Payoh',
    price: 80
  },
  {
    name: 'Aparthotel in Singapore · ★4.89 · 1 bedroom · 1 bed · 1 bath',
    host_name: 'Heritage',
    host_is_superhost: 'True',
    neighbourhood_cleansed: 'Singapore River',
    price: 235
  },
  {
    name: 'Aparthotel in Singapore · ★4.78 · Studio · 1 bed · 1 bath',
    host_name: 'Heritage',
    host_is_superhost: 'True',
    neighbourhood_cleansed: 'Singapore River',
    price: 173
  },
  {
    name: 'Aparthotel in Singapore · ★4.75 · 1 bedroom · 1 bed · 1 bath',
    host_name: 'Heritage',
    host_is_superhost: 'True',
    neighbourhood_cleansed: 'Downtown Core',
    price: 196
  },
  {
    name: 'Rental unit in Singapore · ★4.0 · Studio · 1 bed · 1 bath',
    host_name: 'Heritage',
    host_is_superhost: 'True',
    neighbourhood_cleansed: 'Outram',
    price: 171
  },
  {
    name: 'Aparthotel in Singapore · ★4.73 · Studio · 1 bed · 1 bath',
    host_name: 'Heritage',
    host_is_superhost: 'True',
    neighbourhood_cleansed: 'Singapore River',
    price: 134
  },
  {
    name: 'Aparthotel in Singapore · ★4.83 · Studio · 1 bed · 1 bath',
    host_name: 'Heritage',
    host_is_superhost: 'True',
    neighbourhood_cleansed: 'Outram',
    price: 190
  },
  {
    name: 'Rental unit in Singapore · 1 bedroom · 1 bed · 1 private bath',
    host_name: 'Tryston',
    host_is_superhost: 'True',
    neighbourhood_cleansed: 'Newton',
    price: 90
  },
  {
    name: 'Aparthotel in Singapore · ★4.75 · Studio · 1 bed · 1 bath',
    host_name: 'Heritage',
    host_is_superhost: 'True',
    neighbourhood_cleansed: 'Downtown Core',
    price: 196
  }
]
```
Insights: 
- With the `$or` statement, the query will output listings belonging to either of the two hosts, id's `11390076` and `23336011`.
Then the output was limitied to only projecting  `name`, `price`, `neighbourhood`, `host_name`, and `host_is_superhost`.



4. find all the unique `host_name` values (see [the docs](https://docs.mongodb.com/manual/reference/method/db.collection.distinct/))
Query:
```
   db.listings1.distinct("host_name")
```
Result:
```
[
  'Aaron',         'Abby',                 'Abdul',
  'Accomodation',  'Adam',                 'Addie',
  'Adeline',       'Aden',                 'Adi',
  'Adrian',        'Airena',               'Aj',
  'Akshay',        'Albert',               'Alee',
  'Aleem',         'Alex',                 'Alexander',
  'Alexis',        'Alice',                'Aline',
  'Aliza',         'Allie',                'Alocassia',
  'Aloysius',      'Amanda',               'Amazing',
  'Amber',         'Ammarudin',            'Ananda',
  'Andre',         'Andrew',               'Andy',
  'Ang',           'Angel',                'Angela',
  'Angelina',      'Anie',                 'Anil',
  'Anita & David', 'Ankit',                'Ann',
  'Ann Siang',     'Anna / Chee Kiang',    'Anthony',
  'Antonio',       'Apac',                 'Apple',
  'Aqira',         'Aravin',               'Ark',
  'Armanadurni',   'Asher',                'Ashneil',
  'Ashok',         'Ashraf',               'Ashton',
  'Atlantis',      'Audrey',               'August',
  'Auntie',        'Aure',                 'Ave',
  'Avy',           'Azan',                 'Azlan',
  'B',             'BEAT. Capsule Hostel', 'BEAT. Sports Hostel',
  'Bang',          'Basanth',              'Beat',
  'Belinda',       'Bella',                'Ben',
  'Benedict',      'Benjamin',             'Benny',
  'Berto',         'Betty',                'Beverly',
  'Bi',            'Bill',                 'Bin',
  'Blueground',    'Bob',                  'Brandon',
  'Bryan',         'Buchao',               'Byulee',
  'C L M P',       'Camille',              'Candice',
  'Caroline',      'Carolyn',              'Carrie',
  'Carry',         'Catherine',            'Catie',
  'Celin',
  ... 661 more items
]
```
Insights: 
- This shows the wide range of individuals and businesses within the AirBnB's host community.

5. find all of the places that have more than 2 `beds` in a neighborhood of your choice (referred to as either the `neighborhood` or `neighbourhood_group_cleansed` fields in the data file), ordered by `review_scores_rating` descending
   - only show the `name`, `beds`, `review_scores_rating`, and `price`
   - if your data set only has blanks for all the neighborhood-related fields, or only one neighborhood value in all documents, you may pick another field to filter by - include an explanation and justification for this in your report.
   - if you run out of memory for this query, try filtering `review_scores_rating` that aren't empty (`$ne`); and lastly, if there's still an issue, you can set the `beds` to match exactly 2.
Query:
```
   db.listings1.find({$or: [{neighbourhood_cleansed: "Bukit Timah"}, {neighbourhood_cleansed: "Serangoon"}], beds:{$gt: 2}}, {_id:0, name:1, beds:1, review_scores_rating:1, price:1})
```
Result:
```
[
  {
    name: 'Rental unit in Singapore · 3 bedrooms · 3 beds · 2 baths',
    beds: 3,
    price: 250,
    review_scores_rating: NaN
  },
  {
    name: 'Rental unit in Singapore · ★4.0 · 1 bedroom · 4 beds · Shared half-bath',
    beds: 4,
    price: 130,
    review_scores_rating: 4
  },
  {
    name: 'Condo in Singapore · 3 bedrooms · 3 beds · 2 baths',
    beds: 3,
    price: NaN,
    review_scores_rating: NaN
  },
  {
    name: 'Condo in Singapore · 3 bedrooms · 3 beds · 2 baths',
    beds: 3,
    price: NaN,
    review_scores_rating: NaN
  },
  {
    name: 'Home in Singapore · ★4.73 · 1 bedroom · 4 beds · 1 private bath',
    beds: 4,
    price: NaN,
    review_scores_rating: 4.73
  },
  {
    name: 'Home in Singapore · ★4.76 · 1 bedroom · 3 beds · 1 shared bath',
    beds: 3,
    price: 78,
    review_scores_rating: 4.76
  },
  {
    name: 'Condo in Singapore · 3 bedrooms · 3 beds · 2 baths',
    beds: 3,
    price: 300,
    review_scores_rating: NaN
  },
  {
    name: 'Rental unit in Singapore · 4 bedrooms · 5 beds · 3 baths',
    beds: 5,
    price: 299,
    review_scores_rating: NaN
  }
]
```
Insights: 
- AirBnB listings in these two neighborhoods seem to be more suited towards larger families/parties. Prices also seem to vary throughout listings in these areas.

6. show the number of listings per host
Query:
```
db.listings1.aggregate({$group: {_id: "$host_id", countListings: {$sum: 1}}})
```
Result:
```
[
  { _id: 24808355, countListings: 1 },
  { _id: 520841404, countListings: 1 },
  { _id: 3785191, countListings: 1 },
  { _id: 469978706, countListings: 1 },
  { _id: 550284313, countListings: 1 },
  { _id: 2164025, countListings: 1 },
  { _id: 549099499, countListings: 1 },
  { _id: 12306807, countListings: 1 },
  { _id: 497195, countListings: 1 },
  { _id: 22262735, countListings: 1 },
  { _id: 7636297, countListings: 1 },
  { _id: 459658024, countListings: 1 },
  { _id: 399268777, countListings: 1 },
  { _id: 1368991, countListings: 1 },
  { _id: 544525434, countListings: 1 },
  { _id: 544341239, countListings: 1 },
  { _id: 199153486, countListings: 1 },
  { _id: 543922318, countListings: 2 },
  { _id: 70457435, countListings: 1 },
  { _id: 69005937, countListings: 1 }
]
```


7. find the average `review_scores_rating` per neighborhood, and only show those that are `4` or above, sorted in descending order of rating (see [the docs](https://docs.mongodb.com/manual/reference/operator/aggregation/sort/))
   - if your data set only has blanks in the neighborhood-related fields, or only one neighborhood value in all documents, you may pick another field to break down the listings by - include an explanation and justification for this in your report.

Query:
```
db.listings1.aggregate({$group: {_id: "$neighbourhood_cleansed", avgScores: {$avg: "$review_scores_rating"}}})
db.listings.aggregate([{$group: {_id: "$neighbourhood_cleansed", avgRating: { $avg: "$review_scores_rating" } }},{$match: { avgRating: { $gte: 4 }}},{ $sort: {avgRating: -1 }}])

```
Result:
```
[
  { _id: 'Marina South', avgRating: 4.8175 },
  { _id: 'Mandai', avgRating: 4.17 }
]
```
Insights: 
- This query only demonstrates two neighborhoods that exceed 4.0 review scores rating. This is most likely influenced by the `NaN` values in the `review_scores_rating` column in the dataset.

