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
    @ManyToMany(fetch = FetchType.LAZY, cascade = CascadeType.PERSIST)
    @JoinTable(name = "person_achievement",
                joinColumns ={
                        @JoinColumn(name = "person_user_id", referencedColumnName = "user_id"),
                        @JoinColumn( name = "person_chat_id", referencedColumnName = "chat_id")},
                inverseJoinColumns = @JoinColumn(name = "achievement_id"))
    private Set<Achievement> achievements;
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
    private Long gitlabId;
    public PersonDTO.PersonPKDTO toPersonDTOPK () {return new PersonDTO.PersonPKDTO(personPk.getChatId(),personPk.getUserId());}


}

