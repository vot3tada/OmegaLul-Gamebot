package ru.gamebot.backend.dto;

import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
public class BossDTO {
    private Integer id;
    private String name;
    private String photo;
    private Integer hp;
    private Integer damage;
    private Float luck;
    private Integer moneyReward;
    private Integer expReward;
    private Integer ultaCharge;
    private Integer cleaveRate;
    private Integer ultaRate;
    private Integer itemId;
}
