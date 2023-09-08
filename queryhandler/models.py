from sqlalchemy import (
    Column,
    Integer,
    String,
    JSON,
    DECIMAL,
    ForeignKey,
    DATETIME,
    BigInteger,
    UniqueConstraint
)
from sqlalchemy.orm import declarative_base
from sqlalchemy_file import FileField


# create a base class for declarative models
Base = declarative_base()


class Coin(Base):
    __tablename__ = "coin"

    id = Column(Integer, primary_key=True)
    name = Column(String(50),unique=True,)
    symbol = Column(String(6), unique=True)
    logo = Column(FileField)
    official_links = Column(JSON)
    main_link = Column(String(250), unique=True)
    history_link = Column(String(250), unique=True)
    socials = Column(JSON())
    circulating_supply = Column(DECIMAL())

    def __repr__(self):
        return self.name


class CoinHistory(Base):
    __tablename__ = "coin_history"

    id = Column(Integer, primary_key=True)
    coin = Column(Integer, ForeignKey("coin.id"))
    date = Column(DATETIME())
    market_cap = Column(BigInteger())
    open = Column(DECIMAL())
    rank = Column(Integer())
    low = Column(DECIMAL())
    high = Column(DECIMAL())
    close = Column(DECIMAL())
    volume = Column(DECIMAL())
    time_open = Column(DATETIME())
    time_close = Column(DATETIME())
    time_high = Column(DATETIME())
    time_low = Column(DATETIME())

    def __repr__(self):
        return f"{self.name}, {self.date}"


class CoinGitHubData(Base):
    __tablename__ = "coin_github_data"

    id = Column(Integer, primary_key=True)
    programming_languages = Column(JSON())
    coin = Column(Integer, ForeignKey("coin.id"))
    contributors = Column(String(1024))
    last_release = Column(DATETIME())
    last_update = Column(DATETIME())
    commit_number = Column(BigInteger())

    def __repr__(self):
        return f"{self.coin.name}"


class Tag(Base):
    __tablename__ = "tag"

    id = Column(Integer, primary_key=True)
    title = Column(
        String(50),
        unique=True,
    )

    def __repr__(self):
        return f"{self.title}"


class CoinTag(Base):
    __tablename__ = "coin_tag"

    id = Column(Integer, primary_key=True)
    coin = Column(Integer, ForeignKey("coin.id"))
    tag = Column(Integer, ForeignKey("tag.id"))

    # Define a unique constraint to prevent duplicate combinations of coin and tag
    __table_args__ = (
        UniqueConstraint('coin', 'tag', name='uq_coin_tag_combination'),
    )


    def __repr__(self):
        return f"{self.coin.name}, {self.tag.title}"
