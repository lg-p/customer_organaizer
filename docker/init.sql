\connect handbook

CREATE TABLE customers(
    customer_id                 varchar(9) PRIMARY KEY,
    full_name                   varchar(120) NOT NULL,
    position                    varchar(120) NOT NULL,
    name_of_the_organization    varchar(120) NOT NULL,
    email                       varchar(80) NOT NULL,
    phone                       varchar(11) NOT NULL
);
