package ru.gamebot.backend.models;

import jakarta.persistence.*;
import lombok.*;
import ru.gamebot.backend.dto.PersonDTO;


@Entity
@Table(name = "person")
@Setter
@Getter
@Builder
@AllArgsConstructor
@NoArgsConstructor
public class Person {

    @EmbeddedId
    private PersonPK personPk;


    @Column(name="name")
    private String name;

    @Column(name="experience", nullable = false)
    private Integer experience;

    @Column(name="experienceMultiply")
    private Integer experienceMultiply;

    @Column(name="money", nullable = false)
    private Integer money;

    @Column(name="photo")
    private String photo;

    @Column(name="luck")
    private Float luck;

    @Column(name="luckMultiply")
    private Integer luckMultiply;

    @Column(name="hp")
    private Integer hp;

    @Column(name="damage")
    private Integer damage;

    @Column(name="damageMultiply")
    private Integer damageMultiply;


    public PersonDTO.PersonPKDTO toPersonDTOPK () {return new PersonDTO.PersonPKDTO(personPk.getChatId(),personPk.getUserId());}

}

