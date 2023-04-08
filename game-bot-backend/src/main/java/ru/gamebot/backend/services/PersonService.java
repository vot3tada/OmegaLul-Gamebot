package ru.gamebot.backend.services;

import jakarta.persistence.EntityManager;
import lombok.RequiredArgsConstructor;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.stereotype.Service;
import ru.gamebot.backend.models.Person;
import ru.gamebot.backend.models.PersonPK;
import ru.gamebot.backend.repository.PersonRepository;
import ru.gamebot.backend.util.PersonAlreadyExistsException;
import ru.gamebot.backend.util.PersonNotFoundException;

import java.time.LocalDate;
import java.util.List;
import java.util.Optional;

@Service
@Transactional(readOnly = true)
@RequiredArgsConstructor
public class PersonService {
    private final PersonRepository personRepository;

    public Person getPerson(int chatId, int userId){
        PersonPK personPK = new PersonPK(userId, chatId);
        return personRepository.findById(personPK).orElseThrow(PersonNotFoundException::new);
    }

    public List<Person> getPersonsByChatId(int userId){
         return personRepository.findByPersonPkChatId(userId);
    }
    public List<Person>  getAllPersons (){
        return personRepository.findAll();
    }

    @Transactional
    public void createPerson(Person person) throws PersonAlreadyExistsException{
        if(personRepository.existsById(person.getPersonPk())){
            throw new PersonAlreadyExistsException();
        }
        personRepository.save(person);
    }
    @Transactional
    public void updatePerson(Person person){
        personRepository.save(person);
    }
}
