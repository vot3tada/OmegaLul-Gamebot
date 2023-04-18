package ru.gamebot.backend.dto;

import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
public class AchievementDTO {
    private String id;
    private String name;
    private String photo;
    private Integer condition;
    private String description;
}
