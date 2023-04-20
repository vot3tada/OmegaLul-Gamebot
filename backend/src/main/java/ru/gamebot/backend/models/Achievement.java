package ru.gamebot.backend.models;

import jakarta.persistence.*;
import lombok.Data;
import lombok.NoArgsConstructor;


@Entity
@Data
@NoArgsConstructor
public class Achievement {
    @Id
    private String id;
    private String name;
    private String photo;
    private Integer condition;
    private String description;
}
