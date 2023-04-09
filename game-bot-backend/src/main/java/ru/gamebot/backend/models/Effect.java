package ru.gamebot.backend.models;

import jakarta.persistence.*;
import lombok.Data;

import java.util.Set;

@Entity
@Data
public class Effect {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id;
    @ManyToMany(mappedBy = "itemEffects")
    private Set<Item> effects;
    private String property;
    private Integer value;
}
