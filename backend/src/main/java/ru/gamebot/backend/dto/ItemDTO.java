package ru.gamebot.backend.dto;

import lombok.Data;
import lombok.NoArgsConstructor;
import ru.gamebot.backend.models.Effect;

import java.util.Set;

@Data
@NoArgsConstructor
public class ItemDTO {

    private Integer id;
    private Set<Effect> effects;
    private String name;
    private Integer price;
    private String description;
    private Integer duration;

}
