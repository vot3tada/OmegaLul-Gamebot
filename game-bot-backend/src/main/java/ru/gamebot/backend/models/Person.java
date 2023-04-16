package ru.gamebot.backend.models;

import jakarta.persistence.*;
import lombok.*;
import ru.gamebot.backend.dto.PersonDTO;

@Entity
@Data
public class Person {

    @EmbeddedId
    private PersonPK personPk;

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


}

