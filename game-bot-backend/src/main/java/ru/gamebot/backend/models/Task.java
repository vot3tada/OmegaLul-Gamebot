package ru.gamebot.backend.models;

import jakarta.persistence.*;
import lombok.Data;
import lombok.NoArgsConstructor;

@Entity
@Data
@NoArgsConstructor
public class Task {
    @Id
    @GeneratedValue(strategy= GenerationType.IDENTITY)
    private Integer id;

    private String name;
    private Integer money;
    private Long duration;
    private Integer workerUserId;
    @Basic
    @Temporal(TemporalType.TIMESTAMP)
    private java.util.Date deadline;
    @ManyToOne
    @JoinColumns({@JoinColumn(name = "person_owner_user_id", referencedColumnName = "user_id"), @JoinColumn( name = "person_chat_id", referencedColumnName = "chat_id")})
    private Person person;

}
