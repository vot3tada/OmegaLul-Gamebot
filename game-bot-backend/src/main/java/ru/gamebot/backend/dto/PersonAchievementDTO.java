package ru.gamebot.backend.dto;

import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
public class PersonAchievementDTO {
    private String achievementId;
    private Integer chatId;
    private Integer userId;
}
