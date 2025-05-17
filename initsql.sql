CREATE TABLE students(
    id serial primary key,
    name varchar,
    group_code varchar,
    birthdate date default current_date(),
    created_at timestamp default current_timestamp()
);

CREATE TABLE employee(
    id serial primary key,
    name varchar,
    vacancy varchar default null,
    login varchar,
    password varchar,
    created_at timestamp default current_timestamp()
)