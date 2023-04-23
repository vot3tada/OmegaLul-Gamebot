package ru.gamebot.backend.services;

import lombok.RequiredArgsConstructor;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.stereotype.Service;
import ru.gamebot.backend.dto.PersonDTO;
import ru.gamebot.backend.models.History;
import ru.gamebot.backend.models.HistoryPK;
import ru.gamebot.backend.models.PersonPK;
import ru.gamebot.backend.repository.HistoryRepository;
import ru.gamebot.backend.repository.PersonRepository;
import ru.gamebot.backend.util.exceptions.PersonExceptions.PersonAlreadyExistsException;
import ru.gamebot.backend.util.exceptions.PersonExceptions.PersonChatIdNotFound;
import ru.gamebot.backend.util.exceptions.PersonExceptions.PersonNotFoundException;
import ru.gamebot.backend.util.exceptions.PersonExceptions.PersonNotUpdateException;
import ru.gamebot.backend.util.mappers.PersonMapper;
import ru.gamebot.backend.consumingrest.*;

import java.util.List;


@Service
@Transactional(readOnly = true)
@RequiredArgsConstructor
public class PersonService {
    private final PersonRepository personRepository;
    private final GitlabRestClient gitlabRestClient;
    private final HistoryRepository historyRepository;
    private final PersonMapper personMapper;

    public List<PersonDTO> getPersonsByChatId(int chatId) throws PersonChatIdNotFound {
        var foundPersons = personRepository.findByPersonPkChatId(chatId);
        if (foundPersons.isEmpty()) {
            throw new PersonChatIdNotFound();
        }
        return foundPersons.stream().map(personMapper::personToPersonDTO).toList();
    }

    public List<PersonDTO> getAllPersons() {
        return personRepository.findAll().stream().map(personMapper::personToPersonDTO).toList();
    }

    @Transactional
    public void deletePersonsByChatId(int chatId) throws PersonNotFoundException {
        historyRepository.deleteAllByPersonPersonPkChatId(chatId);
        long result = personRepository.deletePersonByPersonPkChatId(chatId);
        if (result == 0) {
            throw new PersonChatIdNotFound();
        }
    }

    @Transactional
    public void createPerson(PersonDTO personDTO) throws PersonAlreadyExistsException {
        var person = personMapper.personDtoToPerson(personDTO);
        if(personDTO.getGitlabUserName()!=null){
            person.setGitlabId(gitlabRestClient.getGitLabUserId(personDTO.getGitlabUserName()));
        }
        if (personRepository.existsById(person.getPersonPk())) {
            throw new PersonAlreadyExistsException();
        }
        personRepository.save(person);
        historyRepository.save(new History(new HistoryPK(person.getPersonPk().getUserId(), person.getPersonPk().getChatId())));
    }

    @Transactional
    public void updatePerson(PersonDTO personDTO, Integer chatId, Integer userId) throws PersonNotUpdateException {
        personDTO.setPersonPKDTO(new PersonDTO.PersonPKDTO(chatId, userId));
        var foundPerson = personRepository.findById(new PersonPK(chatId, userId))
                                            .orElseThrow(PersonNotFoundException::new);
        if (personDTO.getExperience() != null && foundPerson.getExperience() != null
                                            && foundPerson.getExperience() > personDTO.getExperience()) {
            throw new PersonNotUpdateException("Experience cannot be less than what is already available!");
        }
        var person = personMapper.personDtoToPersonUpdate(personDTO);
        person.setGitlabId(foundPerson.getGitlabId());
        person.setAchievements(foundPerson.getAchievements());
        if(personDTO.getGitlabUserName()!=null){
            person.setGitlabId(gitlabRestClient.getGitLabUserId(personDTO.getGitlabUserName()));
        }
        personRepository.save(person);
    }
}

