from sqlalchemy import SmallInteger, Integer
from sqlalchemy.dialects.mysql import TINYINT

UnsignedTinyInteger = SmallInteger()
UnsignedTinyInteger = UnsignedTinyInteger.with_variant(Integer, "sqlite").with_variant(
    TINYINT(unsigned=True), "mysql", "mariadb"
)
