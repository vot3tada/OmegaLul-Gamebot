package ru.gamebot.backend.util.mappers.EventMapper;

import org.mapstruct.InjectionStrategy;
import org.mapstruct.Mapper;
import ru.gamebot.backend.dto.CreateEventDTO;
import ru.gamebot.backend.models.Event;
@Mapper(
        componentModel = "spring",
        injectionStrategy = InjectionStrategy.CONSTRUCTOR
)
public interface EventMapper {
    Event eventDTOToEvent(CreateEventDTO createEventDTO);

    CreateEventDTO eventToEventDTO(Event event);
    }

