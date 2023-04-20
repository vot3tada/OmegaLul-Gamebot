package ru.gamebot.backend.util.mappers.AchievementMapper;

import org.mapstruct.InjectionStrategy;
import org.mapstruct.Mapper;
import ru.gamebot.backend.dto.AchievementDTO;
import ru.gamebot.backend.models.Achievement;

@Mapper(
        componentModel = "spring",
        injectionStrategy = InjectionStrategy.CONSTRUCTOR
)
public interface AchievementMapper {
    AchievementDTO achievementToAchievementDTO(Achievement achievement);

}
