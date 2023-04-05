package ru.gamebot.backend.models;

import jakarta.persistence.*;
import lombok.Getter;
import lombok.Setter;


@Entity
@Table(name = "person")
@Setter
@Getter
public class Person {

    @EmbeddedId
    private PersonPK personPk;


    @Column(name="name")
    private String name;

    @Column(name="experience")
    private int experience;

    @Column(name="experienceMultiply")
    private int experienceMultiply;

    @Column(name="money")
    private int money;

    @Column(name="photo")
    private String photo;

    @Column(name="luck")
    private float luck;

    @Column(name="luckMultiply")
    private int luckMultiply;

    @Column(name="hp")
    private int hp;

    @Column(name="damage")
    private int damage;

    @Column(name="damageMultiply")
    private int damageMultiply;


}

