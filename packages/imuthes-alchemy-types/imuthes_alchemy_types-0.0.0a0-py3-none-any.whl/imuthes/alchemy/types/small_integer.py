from sqlalchemy import SmallInteger, Integer

SmallInteger = SmallInteger()
SmallInteger = SmallInteger.with_variant(Integer, "sqlite")
