package ru.gamebot.backend.util.mappers;

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
    Person personDtoToPerson(PersonDTO source);

    @Mapping(target = "gitlabId", ignore = true)
    @Mapping(target = "personPk", expression  = "java(source.toPersonPK())")
    @Mapping(target = "achievements", ignore = true)
    Person personDtoToPersonUpdate(PersonDTO source);

    @Mapping(target = "personPKDTO", expression = "java(source.toPersonDTOPK())")
    PersonDTO personToPersonDTO(Person source);
}
