from sqlalchemy import Integer
from sqlalchemy.dialects.mysql import INTEGER

UnsignedInteger = Integer()
UnsignedInteger = UnsignedInteger.with_variant(INTEGER(unsigned=True), "mysql", "mariadb")
