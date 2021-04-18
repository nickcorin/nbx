create table if not exists users (
    id bigint not null auto_increment,
    uuid varchar(255) not null,
    `name` varchar(255) not null,
    `email` varchar(255) not null,
    created_at datetime not null,
    updated_at datetime not null,
    
    unique index unique_uuid(uuid),
    unique index unique_email(email),

    primary key(id)
);