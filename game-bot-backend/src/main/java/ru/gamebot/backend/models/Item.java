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


    @ManyToMany
    @JoinTable(
            name = "item_effects",
            joinColumns = @JoinColumn(name = "item_id"),
            inverseJoinColumns = @JoinColumn(name = "effect_id")
    )
    private Set<Effect> effects;
    @OneToMany(mappedBy = "item")
    private Set<Inventory> inventory;
    private String name;
    private Integer price;
    private String description;
    private Integer duration;
}
