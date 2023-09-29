--drop table if exists create table 
drop table projdata cascade;

--create tables

create table projdata (
	FIPS_Code int,
	States varchar(255),
	Area_Name varchar(255),
	Civilian_labor_force_2020 bigint,
	Employed_2020 bigint,
	Unemployed_2020 bigint,
	Unemployment_rate_2020 decimal,
	Civilian_labor_force_2021 bigint,
	Employed_2021 bigint,
	Unemployed_2021 bigint,
	Unemployment_rate_2021 decimal,
	Civilian_labor_force_2022 bigint,
	Employed_2022 bigint,
	Unemployed_2022 bigint,
	Unemployment_rate_2022 decimal,
	POP_ESTIMATE_2020 bigint,
	POP_ESTIMATE_2021 bigint,
	POP_ESTIMATE_2022 bigint,
	BIRTHS_2020 int,
	BIRTHS_2021 int,
	BIRTHS_2022 int,
	DEATHS_2020 int,
	DEATHS_2021 int,
	DEATHS_2022 int,
	NoHSD int,
	HSD int,
	CAD int,
	BD int
);

select * from projdata

