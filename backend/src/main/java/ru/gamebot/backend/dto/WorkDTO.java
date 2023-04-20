package ru.gamebot.backend.dto;

import jakarta.validation.constraints.NotEmpty;
import jakarta.validation.constraints.NotNull;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
public class WorkDTO {
    private Integer id;
    @NotEmpty(groups = Create.class)
    private String name;
    @NotNull(groups = Create.class)
    private Integer levelRequired;
    @NotNull(groups = Create.class)
    private Integer expReward;
    @NotNull(groups = Create.class)
    private Integer moneyReward;
}
