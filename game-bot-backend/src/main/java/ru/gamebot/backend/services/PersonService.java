package ru.gamebot.backend.services;

import org.springframework.beans.factory.annotation.Autowired;
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
public class PersonService {
    private final PersonRepository personRepository;
    @Autowired
    public PersonService(PersonRepository personRepository){
        this.personRepository = personRepository;
    }

    public Person getPerson(int chatId, int userId){
        PersonPK personPK = new PersonPK(chatId, userId);
        Optional<Person> foundPerson = personRepository.findById(personPK);
        return foundPerson.orElseThrow(PersonNotFoundException::new);
    }

    public List<Person>  getAllPersons (){
        List<Person> allFoundPersons = personRepository.findAll();
        return allFoundPersons;
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
