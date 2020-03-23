drop table if exists user;
drop table if exists post;
drop table if exists skill;
drop table if exists post_skill;

create table user (
    id integer primary key autoincrement,
    username text unique not null,
    password text not null
);

create table post (
    id integer primary key autoincrement,
    author_id integer not null,
    created timestamp not null default current_timestamp,
    title text not null,
    body text not null,
    foreign key (author_id) references user (id)
);

create table skill (
    id integer primary key autoincrement,
    name text not null
);

create table post_skill (
    id integer primary key autoincrement,
    post_id integer not null,
    skill_id integer not null,
    foreign key (post_id) references post (id),
    foreign key (skill_id) references skill (id)
);
