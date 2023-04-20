package ru.gamebot.backend.models;

import jakarta.persistence.*;
import lombok.Data;
import lombok.NoArgsConstructor;

@Entity
@Data
@NoArgsConstructor
public class PersonEvents {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id;
    private Boolean creator = false;

    @ManyToOne
    @JoinColumns({@JoinColumn(name = "person_user_id", referencedColumnName = "user_id"), @JoinColumn(name="person_chat_id", referencedColumnName = "chat_id")})
    private Person person;

    @ManyToOne
    @JoinColumn(name = "event_id", referencedColumnName = "id")
    private Event event;

    public PersonEvents(Boolean creator, Person person, Event event) {
        this.creator = creator;
        this.person = person;
        this.event = event;
    }
}
