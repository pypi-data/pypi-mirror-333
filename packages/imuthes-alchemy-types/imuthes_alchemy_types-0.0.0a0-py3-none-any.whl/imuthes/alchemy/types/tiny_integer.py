from sqlalchemy import SmallInteger, Integer
from sqlalchemy.dialects.mysql import TINYINT

TinyInteger = SmallInteger()
TinyInteger = TinyInteger.with_variant(Integer, "sqlite").with_variant(TINYINT(), "mysql", "mariadb")
