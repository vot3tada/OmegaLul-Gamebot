package ru.gamebot.backend.dto;

import jakarta.validation.constraints.Min;

public class PersonDTO {
    private int chatId;
    private int userId;
    private String name;

    private int experience;


    private int experienceMultiply;

    private int money;

    private String photo;

    private float luck;
    private int luckMultiply;

    private int hp;

    private int damage;
    private int damageMultiply;

    public int getChatId() {
        return chatId;
    }

    public void setChatId(int chatId) {
        this.chatId = chatId;
    }

    public int getUserId() {
        return userId;
    }

    public void setUserId(int userId) {
        this.userId = userId;
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
