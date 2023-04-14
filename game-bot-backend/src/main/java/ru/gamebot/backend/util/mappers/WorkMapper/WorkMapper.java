package ru.gamebot.backend.util.mappers.WorkMapper;

import org.mapstruct.InjectionStrategy;
import org.mapstruct.Mapper;
import ru.gamebot.backend.dto.WorkDTO;
import ru.gamebot.backend.models.Work;

@Mapper(
        componentModel = "spring",
        injectionStrategy = InjectionStrategy.CONSTRUCTOR
)
public interface WorkMapper {

    WorkDTO workToWorkDTO(Work work);

    Work workDTOToWork(WorkDTO workDTO);
}
