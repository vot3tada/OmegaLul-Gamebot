package ru.gamebot.backend.util.mappers.PersonMapper;

import org.mapstruct.Mapper;
import ru.gamebot.backend.dto.PersonDTO;
import ru.gamebot.backend.models.PersonPK;

@Mapper
public interface PersonPKMapper {
    PersonPK toPersonDTOPK(PersonDTO.PersonPKDTO personPKDTO);
    PersonDTO.PersonPKDTO toPersonPK(PersonPK personPKDTO);
}
