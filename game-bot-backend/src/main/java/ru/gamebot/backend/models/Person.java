package ru.gamebot.backend.models;

import jakarta.persistence.*;


@Entity
@Table(name = "person")
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

    public PersonPK getPersonPk() {
        return personPk;
    }

    public void setPersonPk(PersonPK personPk) {
        this.personPk = personPk;
    }
    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public int getExperience() {
        return experience;
    }

    public void setExperience(int experience) {
        this.experience = experience;
    }

    public int getExperienceMultiply() {
        return experienceMultiply;
    }

    public void setExperienceMultiply(int experienceMultiply) {
        this.experienceMultiply = experienceMultiply;
    }

    public int getMoney() {
        return money;
    }

    public void setMoney(int money) {
        this.money = money;
    }

    public String getPhoto() {
        return photo;
    }

    public void setPhoto(String photo) {
        this.photo = photo;
    }

    public float getLuck() {
        return luck;
    }

    public void setLuck(float luck) {
        this.luck = luck;
    }

    public int getLuckMultiply() {
        return luckMultiply;
    }

    public void setLuckMultiply(int luckMultiply) {
        this.luckMultiply = luckMultiply;
    }

    public int getHp() {
        return hp;
    }

    public void setHp(int hp) {
        this.hp = hp;
    }

    public int getDamage() {
        return damage;
    }

    public void setDamage(int damage) {
        this.damage = damage;
    }

    public int getDamageMultiply() {
        return damageMultiply;
    }

    public void setDamageMultiply(int damageMultiply) {
        this.damageMultiply = damageMultiply;
    }



}

