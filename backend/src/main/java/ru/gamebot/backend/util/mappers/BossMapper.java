package ru.gamebot.backend.util.mappers;

import org.mapstruct.InjectionStrategy;
import org.mapstruct.Mapper;
import org.mapstruct.Mapping;
import ru.gamebot.backend.dto.BossDTO;
import ru.gamebot.backend.models.Boss;

@Mapper(
        componentModel = "spring",
        injectionStrategy = InjectionStrategy.CONSTRUCTOR
)
public interface BossMapper {
    @Mapping(target = "itemId", expression = "java(boss.getItem().getId())")
    BossDTO bossToBossDTO(Boss boss);
}
