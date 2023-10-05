import random
from sqlalchemy import create_engine, Column, Integer, String, desc, not_
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

engine = create_engine('sqlite:///C:\\Users\\benny\\Github\\ipc-county\\src\\db\\project3.sqlite', echo=True)
Base = declarative_base()
diplomas = [ 'NoHSB', 'HSB', 'CAD', 'BD']
state_abbreviations = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA", "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]


class CountyData(Base):
    __tablename__ = 'counties'

    id = Column(Integer, primary_key=True)
    FIPS_Code = Column(Integer)
    States = Column(String)
    Area_Name = Column(String)
    laborforce_2020 = Column(Integer)
    Employed_2020 = Column(Integer)
    Unemployed_2020 = Column(Integer)
    Unemployment_rate_2020 = Column(Integer)
    laborforce_2021 = Column(Integer)
    Employed_2021 = Column(Integer)
    Unemployed_2021 = Column(Integer)
    Unemployment_rate_2021 = Column(Integer)
    laborforce_2022 = Column(Integer)
    Employed_2022 = Column(Integer)
    Unemployed_2022 = Column(Integer)
    Unemployment_rate_2022 = Column(Integer)
    POP_2020 = Column(Integer)
    POP_2021 = Column(Integer)
    POP_2022 = Column(Integer)
    BIRTHS_2020 = Column(Integer)
    BIRTHS_2021 = Column(Integer)
    BIRTHS_2022 = Column(Integer)
    DEATHS_2020 = Column(Integer)
    DEATHS_2021 = Column(Integer)
    DEATHS_2022 = Column(Integer)
    NoHSB = Column(Integer)
    HSB = Column(Integer)
    CAD = Column(Integer)
    BD = Column(Integer)



def get_map_data(sqlVar):
    Session = sessionmaker(bind=engine)
    session = Session()
    if sqlVar.split('_')[0] in diplomas:
        sqlVar = sqlVar.split('_')[0]
    column = getattr(CountyData, sqlVar)
    results = session.query(CountyData.FIPS_Code, column).all()
    county_data_map = {fips: column for fips, column in results}
    session.close()

    return county_data_map


def get_bar_data(sqlVar):
    Session = sessionmaker(bind=engine)
    session = Session()

    tableVar = sqlVar.split('_')[0]

    if tableVar in diplomas:
        
        query = [getattr(CountyData, x) for x in diplomas]
        query.append(CountyData.Area_Name)
    else:
        col1 = getattr(CountyData, f"{tableVar}_2020")
        col2 = getattr(CountyData, f"{tableVar}_2021")
        col3 = getattr(CountyData, f"{tableVar}_2022")
        query = [CountyData.Area_Name, col1, col2, col3]

   
    if tableVar in diplomas: 
        results = session.query(*query).order_by(desc(getattr(CountyData,tableVar))).filter(not_(CountyData.FIPS_Code.like('%000'))).limit(10).all()
        county_data_array = {Area_Name: (NoHSB, HSB, CAD, BD) for NoHSB, HSB, CAD, BD, Area_Name in results}
    else:
        results = session.query(*query).order_by(desc(getattr(CountyData, sqlVar))).filter(not_(CountyData.FIPS_Code.like('%000'))).limit(10).all()
        county_data_array = {Area_Name: (col1, col2, col3) for Area_Name, col1, col2, col3 in results}
    session.close()
    return county_data_array

def get_scatter_data(sqlVar):
    Session = sessionmaker(bind=engine)
    session = Session()

    selected_states = random.sample(state_abbreviations, 5)
    year = sqlVar.split('_')[1]
    if sqlVar.split('_')[0] in diplomas:
        sqlVar = sqlVar.split('_')[0]
    column = getattr(CountyData, sqlVar)
    compare = getattr(CountyData, f'Unemployment_rate_{year}')
    pop = getattr(CountyData, f'POP_{year}')

    results = session.query(CountyData.FIPS_Code, CountyData.States, compare, pop/column).filter(not_(CountyData.FIPS_Code.like('%000')), CountyData.States.in_(selected_states)).all()
    county_data_scatter = {code: (states, compare, per) for code, states, compare, per in results}
    session.close()

    print(county_data_scatter)

    return county_data_scatter