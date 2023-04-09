package ru.gamebot.backend.services;

import lombok.RequiredArgsConstructor;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.stereotype.Service;
import ru.gamebot.backend.models.Person;
import ru.gamebot.backend.models.PersonPK;
import ru.gamebot.backend.repository.PersonRepository;
import ru.gamebot.backend.util.PersonExceptions.PersonAlreadyExistsException;
import ru.gamebot.backend.util.PersonExceptions.PersonChatIdNotFound;
import ru.gamebot.backend.util.PersonExceptions.PersonNotFoundException;

import java.util.List;

@Service
@Transactional(readOnly = true)
@RequiredArgsConstructor
public class PersonService {
    private final PersonRepository personRepository;

    public Person getPerson(int chatId, int userId){
        PersonPK personPK = new PersonPK(userId, chatId);
        return personRepository.findById(personPK).orElseThrow(PersonNotFoundException::new);
    }

    public List<Person> getPersonsByChatId(int chatId) throws PersonChatIdNotFound{
        List<Person> foundPersons = personRepository.findByPersonPkChatId(chatId);
        if(foundPersons.isEmpty()){
            throw new PersonChatIdNotFound();
        }
         return foundPersons;
    }
    public List<Person>  getAllPersons (){
        return personRepository.findAll();
    }

    @Transactional
    public void deletePersonsByChatId(int chatId) throws PersonNotFoundException{
        long result = personRepository.deletePersonByPersonPkChatId(chatId);
        if (result == 0) {
            throw new PersonChatIdNotFound();
        }
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
