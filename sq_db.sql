CREATE TABLE IF NOT EXISTS log (
id integer PRIMARY KEY AUTOINCREMENT,
data_order text NOT NULL,
name_customer text NOT NULL,
brand_car text NOT NULL,
number_car text NOT NULL,
text_order text NOT NULL
);
