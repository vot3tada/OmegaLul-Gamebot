package ru.gamebot.backend.models;

import jakarta.persistence.*;
import lombok.Data;


@Entity
@Data
public class Effect {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id;
    private String property;
    private Integer value;
}
