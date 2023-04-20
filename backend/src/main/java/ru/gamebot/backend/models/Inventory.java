package ru.gamebot.backend.models;

import jakarta.persistence.*;
import lombok.Data;
import lombok.NoArgsConstructor;


@Entity
@Data
@NoArgsConstructor
public class Inventory {
    @Id
    @GeneratedValue(strategy=GenerationType.IDENTITY)
    private Integer id;
    @ManyToOne
    @JoinColumns({@JoinColumn(name = "person_user_id", referencedColumnName = "user_id"), @JoinColumn(name="person_chat_id", referencedColumnName = "chat_id")})
    private Person person;


    @ManyToOne
    @JoinColumn(name = "item_id")
    private Item item;
    private Integer count;

    public Inventory(Item item, Integer count, Person person) {
        this.item = item;
        this.count = count;
        this.person = person;
    }
}
