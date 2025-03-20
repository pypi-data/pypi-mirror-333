from sqlalchemy import SmallInteger, Integer
from sqlalchemy.dialects.mysql import SMALLINT

UnsignedSmallInteger = SmallInteger()
UnsignedSmallInteger = UnsignedSmallInteger.with_variant(Integer, "sqlite").with_variant(
    SMALLINT(unsigned=True), "mysql", "mariadb"
)
