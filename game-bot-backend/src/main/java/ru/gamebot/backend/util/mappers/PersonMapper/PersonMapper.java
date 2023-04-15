package ru.gamebot.backend.util.mappers.PersonMapper;

import org.mapstruct.InjectionStrategy;
import org.mapstruct.Mapper;
import org.mapstruct.Mapping;
import ru.gamebot.backend.dto.PersonDTO;
import ru.gamebot.backend.models.Person;

@Mapper(
        componentModel = "spring",
        injectionStrategy = InjectionStrategy.CONSTRUCTOR,
        uses = {PersonPKMapper.class}
)
public interface PersonMapper {
    @Mapping(target = "personPk", expression  = "java(source.toPersonPK())")
    @Mapping(target = "experienceMultiply", source = "experienceMultiply", defaultValue = "1")
    @Mapping(target = "luck", source = "luck", defaultValue = "0.2F")
    @Mapping(target = "luckMultiply", source = "luckMultiply", defaultValue = "1")
    @Mapping(target = "hp", source = "hp", defaultValue = "100")
    @Mapping(target = "damage", source = "damage", defaultValue = "20")
    @Mapping(target = "damageMultiply", source = "damageMultiply", defaultValue = "1")
    @Mapping(target = "inventory", ignore = true)
    Person personDtoToPerson(PersonDTO source);

    @Mapping(target = "personPKDTO", expression = "java(source.toPersonDTOPK())")
    PersonDTO personToPersonDTO(Person source);
}
