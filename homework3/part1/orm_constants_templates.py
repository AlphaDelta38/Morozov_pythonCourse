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


def create_enum(key, enums, additional=""):
    return f"CHECK ({key} IN ({', '.join(map(lambda x: f'\"{x}\"', enums))}) {additional})"


def create_uniques(tables):
    return f"UNIQUE({', '.join(tables)})"


def create_varchar(n):
    return f"VARCHAR({max(min(255, n), 1)})"


def create_default(value):
    return f"DEFAULT {value}"
