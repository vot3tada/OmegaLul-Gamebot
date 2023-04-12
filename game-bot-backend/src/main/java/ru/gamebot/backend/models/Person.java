package ru.gamebot.backend.models;

import jakarta.persistence.*;
import lombok.*;
import ru.gamebot.backend.dto.PersonDTO;

import java.util.Set;


@Entity
@Data
public class Person {

    @EmbeddedId
    private PersonPK personPk;

    @OneToMany(mappedBy = "person",cascade = CascadeType.ALL)
    private Set<Inventory> inventory;

    private String name;


    private Integer experience;


    private Integer experienceMultiply;

    private Integer money;


    private String photo;


    private Float luck;

    private Integer luckMultiply;


    private Integer hp;


    private Integer damage;


    private Integer damageMultiply;


    public PersonDTO.PersonPKDTO toPersonDTOPK () {return new PersonDTO.PersonPKDTO(personPk.getChatId(),personPk.getUserId());}


    @Override
    public String toString() {
        return "Person{" +
                "personPk=" + personPk +
                ", inventory=" + inventory +
                ", name='" + name + '\'' +
                ", experience=" + experience +
                ", experienceMultiply=" + experienceMultiply +
                ", money=" + money +
                ", photo='" + photo + '\'' +
                ", luck=" + luck +
                ", luckMultiply=" + luckMultiply +
                ", hp=" + hp +
                ", damage=" + damage +
                ", damageMultiply=" + damageMultiply +
                '}';
    }
}

