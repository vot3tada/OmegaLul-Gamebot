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
import ru.gamebot.backend.util.exceptions.EventExceptions.ChatNotFoundException;
import ru.gamebot.backend.util.exceptions.EventExceptions.EventAlreadyExistException;
import ru.gamebot.backend.util.exceptions.EventExceptions.EventNotFoundException;
import ru.gamebot.backend.util.exceptions.PersonExceptions.PersonNotFoundException;
import ru.gamebot.backend.util.mappers.EventMapper.EventMapper;

import java.sql.Timestamp;
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
        return new GetEventDTO(event.getName(),event.getStartedAt(),convertToPersonEventsDTO(members), id);
    }

    public List<GetEventDTO> getEventsByChatId(Integer chatId) throws ChatNotFoundException {
        var eventsDTO = new ArrayList<GetEventDTO>();
        var personEvents = personEventsRepository.findAllEventByPersonPersonPkChatIdAndEventStartedAtAfterOrderByEventDesc(chatId, new Timestamp(System.currentTimeMillis()));
        if(personEvents == null){
            throw new ChatNotFoundException("Chat not found!");
        }
        for(PersonEvents personEvent : personEvents){
            var event  = personEvent.getEvent();
            eventsDTO.add(new GetEventDTO(event.getName(),event.getStartedAt(),event.getId()));
        }
        return eventsDTO;
    }
    @Transactional
    public GetEventDTO createEvent(CreateEventDTO createEventDTO) throws EventAlreadyExistException{
        var event = eventMapper.eventDTOToEvent(createEventDTO);
        if(eventRepository.existsByNameAndStartedAt(event.getName(),event.getStartedAt())){
            throw new EventAlreadyExistException("This event already exists!");
        }
        var person = personRepository.findById(new PersonPK(createEventDTO.getChatId(), createEventDTO.getUserId())).orElseThrow(PersonNotFoundException::new);
        var savedEvent = eventRepository.save(event);
        personEventsRepository.save(new PersonEvents(true, person,event));
        return new GetEventDTO(savedEvent.getName(),savedEvent.getStartedAt(),savedEvent.getId());
    }
    @Transactional
    public void addMember(CreateEventDTO eventDTO){
        var event = eventRepository.findById(eventDTO.getId()).orElseThrow(EventNotFoundException::new);
        var person = personRepository.findById(new PersonPK(eventDTO.getChatId(),eventDTO.getUserId())).orElseThrow(PersonNotFoundException::new);
        personEventsRepository.save(new PersonEvents(false,person,event));
    }

    @Transactional
    public void deleteMember(CreateEventDTO eventDTO){
        var event = eventRepository.findById(eventDTO.getId()).orElseThrow(EventNotFoundException::new);
        var person = personRepository.findById(new PersonPK(eventDTO.getChatId(),eventDTO.getUserId())).orElseThrow(PersonNotFoundException::new);
        personEventsRepository.deleteByEventAndPerson(event, person);
    }

    private List<PersonEventsDTO> convertToPersonEventsDTO(List<PersonEvents> personEvents){
        var personEventsDTO = new ArrayList<PersonEventsDTO>();
        for(PersonEvents pe : personEvents){
            personEventsDTO.add(new PersonEventsDTO(pe.getCreator(),pe.getPerson().getPersonPk().getChatId(), pe.getPerson().getPersonPk().getUserId()));
        }
        return personEventsDTO;
    }
}
