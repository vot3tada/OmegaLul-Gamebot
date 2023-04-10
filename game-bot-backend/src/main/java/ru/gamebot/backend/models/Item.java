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


    @OneToMany(mappedBy = "item")
    private Set<Effect> effects;
    private String name;
    private Integer price;
    private String description;
    private Integer duration;

}
