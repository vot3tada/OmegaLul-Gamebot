package ru.gamebot.backend.services;

import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import ru.gamebot.backend.dto.EventDTO;
import ru.gamebot.backend.models.PersonEvents;
import ru.gamebot.backend.models.PersonPK;
import ru.gamebot.backend.repository.EventRepository;
import ru.gamebot.backend.repository.PersonEventsRepository;
import ru.gamebot.backend.repository.PersonRepository;
import ru.gamebot.backend.util.exceptions.PersonExceptions.PersonNotFoundException;
import ru.gamebot.backend.util.mappers.EventMapper.EventMapper;

@Service
@Transactional(readOnly = true)
@RequiredArgsConstructor
public class EventService {
    private final EventRepository eventRepository;
    private final PersonEventsRepository personEventsRepository;
    private final PersonRepository personRepository;
    private final EventMapper eventMapper;

    @Transactional
    public void createEvent(EventDTO eventDTO){
        var event = eventMapper.eventDTOToEvent(eventDTO);
        var person = personRepository.findById(new PersonPK(eventDTO.getChatId(),eventDTO.getUserId())).orElseThrow(PersonNotFoundException::new);
        eventRepository.save(event);
        personEventsRepository.save(new PersonEvents(true, person,event));
    }
}
