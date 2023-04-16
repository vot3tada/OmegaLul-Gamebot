package ru.gamebot.backend.services;

import lombok.RequiredArgsConstructor;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.stereotype.Service;
import ru.gamebot.backend.dto.PersonDTO;
import ru.gamebot.backend.models.History;
import ru.gamebot.backend.models.HistoryPK;
import ru.gamebot.backend.models.Person;
import ru.gamebot.backend.models.PersonPK;
import ru.gamebot.backend.repository.PersonRepository;
import ru.gamebot.backend.util.exceptions.PersonExceptions.PersonAlreadyExistsException;
import ru.gamebot.backend.util.exceptions.PersonExceptions.PersonChatIdNotFound;
import ru.gamebot.backend.util.exceptions.PersonExceptions.PersonNotFoundException;
import ru.gamebot.backend.util.exceptions.PersonExceptions.PersonNotUpdateException;
import ru.gamebot.backend.util.mappers.PersonMapper.PersonMapper;

import java.util.ArrayList;
import java.util.List;


@Service
@Transactional(readOnly = true)
@RequiredArgsConstructor
public class PersonService {
    private final PersonRepository personRepository;
    private final PersonMapper personMapper;

    public List<PersonDTO> getPersonsByChatId(int chatId) throws PersonChatIdNotFound {
        var foundPersons = personRepository.findByPersonPkChatId(chatId);
        if (foundPersons.isEmpty()) {
            throw new PersonChatIdNotFound();
        }
        return convertToListPersonDTO(foundPersons);
    }

    public List<PersonDTO> getAllPersons() {
        return convertToListPersonDTO(personRepository.findAll());
    }

    @Transactional
    public void deletePersonsByChatId(int chatId) throws PersonNotFoundException {
        long result = personRepository.deletePersonByPersonPkChatId(chatId);
        if (result == 0) {
            throw new PersonChatIdNotFound();
        }
    }

    @Transactional
    public void createPerson(PersonDTO personDTO) throws PersonAlreadyExistsException {
        var person = personMapper.personDtoToPerson(personDTO);
        if (personRepository.existsById(person.getPersonPk())) {
            throw new PersonAlreadyExistsException();
        }
        person.setHistory(new History(new HistoryPK(person.getPersonPk().getUserId(),person.getPersonPk().getChatId())));
        personRepository.save(person);
    }

    @Transactional
    public void updatePerson(PersonDTO personDTO, Integer chatId, Integer userId) throws PersonNotUpdateException {
        var personPK = new PersonPK(chatId, userId);
        personDTO.setPersonPKDTO(new PersonDTO.PersonPKDTO(chatId, userId));
        var foundPerson = personRepository.findById(personPK).orElseThrow(PersonNotFoundException::new);
        if (personDTO.getExperience() != null && foundPerson.getExperience() != null && foundPerson.getExperience() > personDTO.getExperience()) {
            throw new PersonNotUpdateException("Experience cannot be less than what is already available!");
        }
        var person = personMapper.personDtoToPerson(personDTO);
        personRepository.save(person);
    }

    private List<PersonDTO> convertToListPersonDTO(List<Person> persons) {
        List<PersonDTO> personDTOS = new ArrayList<>();
        for (Person person : persons) {
            personDTOS.add(personMapper.personToPersonDTO(person));
        }
        return personDTOS;
    }
}

