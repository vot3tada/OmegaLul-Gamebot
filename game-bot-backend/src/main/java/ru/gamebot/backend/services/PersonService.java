package ru.gamebot.backend.services;

import lombok.RequiredArgsConstructor;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.stereotype.Service;
import ru.gamebot.backend.models.Person;
import ru.gamebot.backend.models.PersonPK;
import ru.gamebot.backend.repository.PersonRepository;
import ru.gamebot.backend.util.PersonNotFoundException;

import java.util.List;
import java.util.Optional;

@Service
@Transactional(readOnly = true)
@RequiredArgsConstructor
public class PersonService {
    private final PersonRepository personRepository;

    public Person getPerson(int chatId, int userId){
        PersonPK personPK = new PersonPK(chatId, userId);
        Optional<Person> foundPerson = personRepository.findById(personPK);
        return foundPerson.orElseThrow(PersonNotFoundException::new);
    }

    public List<Person> getPersonsByChatId(int userId){
         return personRepository.findByPersonPkChatId(userId);
    }
    public List<Person>  getAllPersons (){
        return personRepository.findAll();
    }

    @Transactional
    public void createPerson(Person person){
        personRepository.save(person);
    }
    @Transactional
    public void updatePerson(Person person){
        personRepository.save(person);
    }
}
