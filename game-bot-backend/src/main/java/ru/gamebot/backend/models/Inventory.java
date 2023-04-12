package ru.gamebot.backend.models;

import jakarta.persistence.*;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.Objects;

@Entity
@Data
@NoArgsConstructor
public class Inventory {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id;
    @ManyToOne
    @JoinColumns({@JoinColumn(name = "person_id_userid"), @JoinColumn(name="person_id_chatid")})
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

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        Inventory inventory = (Inventory) o;
        return Objects.equals(id, inventory.id) && Objects.equals(person, inventory.person) && Objects.equals(item, inventory.item) && Objects.equals(count, inventory.count);
    }

    @Override
    public int hashCode() {
        return Objects.hash(id, person, item, count);
    }
}
