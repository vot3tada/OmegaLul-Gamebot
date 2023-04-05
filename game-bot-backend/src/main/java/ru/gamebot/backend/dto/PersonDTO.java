package ru.gamebot.backend.dto;

import jakarta.validation.constraints.NotEmpty;
import jakarta.validation.constraints.NotNull;
import lombok.Getter;
import lombok.Setter;

@Setter
@Getter
public class PersonDTO {
    @NotNull(groups = CreatePerson.class)
    private int chatId;
    @NotNull(groups = CreatePerson.class)
    private int userId;
    @NotEmpty(groups = CreatePerson.class)
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

}
