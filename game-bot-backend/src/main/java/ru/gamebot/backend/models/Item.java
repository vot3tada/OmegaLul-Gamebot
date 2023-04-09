package ru.gamebot.backend.models;

import jakarta.persistence.*;
import lombok.Data;

import java.util.Set;

@Entity
@Data
public class Item{

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id;

    @ManyToMany(cascade = CascadeType.ALL)
    @JoinTable(
            name="item_effect", joinColumns = @JoinColumn(name="item_id"),
            inverseJoinColumns = @JoinColumn(name="effect_id")
    )
    private Set<Effect> itemEffects;
    private String name;
    private Integer price;
    private String description;
    private Integer duration;

    private void addEffect(Effect effect) {
        this.itemEffects.add(effect);
    }
}
