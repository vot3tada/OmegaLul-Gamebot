package ru.gamebot.backend.models;

import jakarta.persistence.*;
import lombok.Data;


@Entity
@Data
public class Effect {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id;
    @ManyToOne(cascade = CascadeType.ALL, fetch = FetchType.LAZY)
    @JoinColumn(name= "item_id", nullable = false)
    private Item item;
    private String property;
    private Integer value;
}
