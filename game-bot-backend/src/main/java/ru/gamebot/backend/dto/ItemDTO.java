package ru.gamebot.backend.dto;

import lombok.Data;
import ru.gamebot.backend.models.Effect;

import java.util.Set;

@Data
public class ItemDTO {
    private Set<Effect> itemEffects;
    private String name;
    private Integer price;
    private String description;
    private Integer duration;

}
