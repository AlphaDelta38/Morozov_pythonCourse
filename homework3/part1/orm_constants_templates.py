## // Action templates // ##
CREATE_TEMPLATE = "CREATE TABLE IF NOT EXISTS"
INSERT_TEMPLATE = "INSERT INTO"
UPDATE_TEMPLATE = "UPDATE"
DELETE_TEMPLATE = "DELETE FROM"
SELECT_TEMPLATE = "SELECT * FROM"

## // type constants // ##
INTEGER = "INTEGER"
TEXT = "TEXT"

## // Attribute constants // ##
PRIMARY_KEY = "PRIMARY KEY"
NOT_NULL = "NOT NULL"
UNIQUE = "UNIQUE"
REAL = "REAL"


## // functions Attribute constants // ##
ENUM = lambda key, enums, additional = "": f"CHECK ({key} IN ({', '.join(map(lambda x: f'\"{x}\"', enums))}) {additional})"
UNIQUES = lambda tables: f", UNIQUE({', '.join(tables)})"
VARCHAR = lambda n: f"VARCHAR({max(min(255, n), 1)})"
DEFAULT = lambda value: f"DEFAULT {value}"
