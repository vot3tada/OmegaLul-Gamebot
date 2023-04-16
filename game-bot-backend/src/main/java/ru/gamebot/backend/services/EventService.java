package ru.gamebot.backend.services;

import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import ru.gamebot.backend.dto.CreateEventDTO;
import ru.gamebot.backend.dto.GetEventDTO;
import ru.gamebot.backend.dto.PersonEventsDTO;
import ru.gamebot.backend.models.PersonEvents;
import ru.gamebot.backend.models.PersonPK;
import ru.gamebot.backend.repository.EventRepository;
import ru.gamebot.backend.repository.PersonEventsRepository;
import ru.gamebot.backend.repository.PersonRepository;
import ru.gamebot.backend.util.exceptions.EventExceptions.EventNotFoundException;
import ru.gamebot.backend.util.exceptions.PersonExceptions.PersonNotFoundException;
import ru.gamebot.backend.util.mappers.EventMapper.EventMapper;

import java.util.ArrayList;
import java.util.List;

@Service
@Transactional(readOnly = true)
@RequiredArgsConstructor
public class EventService {
    private final EventRepository eventRepository;
    private final PersonEventsRepository personEventsRepository;
    private final PersonRepository personRepository;
    private final EventMapper eventMapper;

    public GetEventDTO getEventById(Integer id){
        var event = eventRepository.findById(id).orElseThrow(EventNotFoundException::new);
        var members = personEventsRepository.findAllByEvent(event);
        return new GetEventDTO(event.getName(),event.getStartedAt(),convertToPersonEventsDTO(members));
    }
    @Transactional
    public void createEvent(CreateEventDTO createEventDTO){
        var event = eventMapper.eventDTOToEvent(createEventDTO);
        var person = personRepository.findById(new PersonPK(createEventDTO.getChatId(), createEventDTO.getUserId())).orElseThrow(PersonNotFoundException::new);
        eventRepository.save(event);
        personEventsRepository.save(new PersonEvents(true, person,event));
    }

    private List<PersonEventsDTO> convertToPersonEventsDTO(List<PersonEvents> personEvents){
        var personEventsDTO = new ArrayList<PersonEventsDTO>();
        for(PersonEvents pe : personEvents){
            personEventsDTO.add(new PersonEventsDTO(pe.getCreator(),pe.getPerson().getPersonPk().getChatId(), pe.getPerson().getPersonPk().getUserId()));
        }
        return personEventsDTO;
    }
}
