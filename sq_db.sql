CREATE TABLE IF NOT EXISTS log (
id integer PRIMARY KEY AUTOINCREMENT,
data_order text NOT NULL,
name_customer text NOT NULL,
brand_car text NOT NULL,
number_car text NOT NULL,
text_order text NOT NULL
);


CREATE TABLE IF NOT EXISTS stock_plus (
id integer PRIMARY KEY AUTOINCREMENT,
name text NOT NULL,
quantity integer NOT NULL,
price_unit integer NOT NULL
);


CREATE TABLE IF NOT EXISTS stock_minus (
id integer PRIMARY KEY AUTOINCREMENT,
name text NOT NULL,
quantity integer NOT NULL,
price_unit integer NOT NULL
);


CREATE TABLE IF NOT EXISTS employees (
id integer PRIMARY KEY AUTOINCREMENT,
name text NOT NULL,
profession text NOT NULL
);


CREATE TABLE IF NOT EXISTS act_foreign_key (
id integer PRIMARY KEY AUTOINCREMENT,
data_order text NOT NULL,
data_act text NOT NULL,
number_car text NOT NULL
);


CREATE TABLE IF NOT EXISTS act_work (
id integer PRIMARY KEY AUTOINCREMENT,
act_id int NOT NULL,
work_completed text NOT NULL,
name_work text NOT NULL,
price_work int NOT NULL,
FOREIGN KEY (act_id) REFERENCES act_foreign_key (id)
);


CREATE TABLE IF NOT EXISTS act_materials (
id integer PRIMARY KEY AUTOINCREMENT,
act_id int NOT NULL,
materials text NOT NULL,
price_materials int NOT NULL,
quantity int NOT NULL,
FOREIGN KEY (act_id) REFERENCES act_foreign_key (id)
);

