CREATE TABLE products (
    id INTEGER PRIMARY  KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    quantity  INTEGER NOT NULL DEFAULT 0,
    price FLOAT NOT NULL

    

)