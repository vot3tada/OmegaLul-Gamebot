package ru.gamebot.backend.services;

import lombok.RequiredArgsConstructor;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.stereotype.Service;
import ru.gamebot.backend.dto.InventoryDTO;
import ru.gamebot.backend.dto.PersonDTO;
import ru.gamebot.backend.models.Inventory;
import ru.gamebot.backend.models.Person;
import ru.gamebot.backend.models.PersonPK;
import ru.gamebot.backend.repository.InventoryRepository;
import ru.gamebot.backend.repository.ItemRepository;
import ru.gamebot.backend.repository.PersonRepository;
import ru.gamebot.backend.util.ItemNotFoundException;
import ru.gamebot.backend.util.PersonExceptions.PersonAlreadyExistsException;
import ru.gamebot.backend.util.PersonExceptions.PersonChatIdNotFound;
import ru.gamebot.backend.util.PersonExceptions.PersonNotFoundException;
import ru.gamebot.backend.util.PersonExceptions.PersonNotUpdateException;
import ru.gamebot.backend.util.PersonMapper.PersonMapper;

import java.util.ArrayList;
import java.util.List;


@Service
@Transactional(readOnly = true)
@RequiredArgsConstructor
public class PersonService {
    private final PersonRepository personRepository;
    private final ItemRepository itemRepository;
    private final InventoryRepository inventoryRepository;
    private final PersonMapper personMapper;

    public List<PersonDTO> getPersonsByChatId(int chatId) throws PersonChatIdNotFound{
        var foundPersons = personRepository.findByPersonPkChatId(chatId);
        if(foundPersons.isEmpty()){
            throw new PersonChatIdNotFound();
        }
         return convertToListPersonDTO(foundPersons);
    }
    public List<PersonDTO>  getAllPersons (){
        return convertToListPersonDTO(personRepository.findAll());
    }

    @Transactional
    public void deletePersonsByChatId(int chatId) throws PersonNotFoundException{
        long result = personRepository.deletePersonByPersonPkChatId(chatId);
        if (result == 0) {
            throw new PersonChatIdNotFound();
        }
    }
    @Transactional
    public void createPerson(PersonDTO personDTO) throws PersonAlreadyExistsException{
        var person = personMapper.personDtoToPerson(personDTO);
        if(personRepository.existsById(person.getPersonPk())){
            throw new PersonAlreadyExistsException();
        }
        personRepository.save(person);
    }
    @Transactional
    public void updatePerson(PersonDTO personDTO, Integer chatId, Integer userId) throws PersonNotUpdateException{
        var personPK = new PersonPK(chatId, userId);
        personDTO.setPersonPKDTO(new PersonDTO.PersonPKDTO(chatId, userId));
        var foundPerson = personRepository.findById(personPK).orElseThrow(PersonNotFoundException::new);
        if (personDTO.getExperience()!=null && foundPerson.getExperience()!=null && foundPerson.getExperience() > personDTO.getExperience()){
            throw new PersonNotUpdateException("Experience cannot be less than what is already available!");
        }
        var person = personMapper.personDtoToPerson(personDTO);
        addInventory(personDTO, person);
        personRepository.save(person);
    }

    private List<PersonDTO> convertToListPersonDTO(List<Person> persons){
        List<PersonDTO> personDTOS = new ArrayList<>();
        for(Person person: persons){
            personDTOS.add(personMapper.personToPersonDTO(person));
        }
        return  personDTOS;
    }

    private void addInventory(PersonDTO personDTO, Person person){
        for(InventoryDTO invDTO : personDTO.getInventoryDTO()){
            var item = itemRepository.findById(invDTO.getId()).orElseThrow(ItemNotFoundException::new);
            var invetoryItem = inventoryRepository.findInventoryByItem_Id(invDTO.getId());
            if (invetoryItem == null){
                inventoryRepository.save(new Inventory(item, invDTO.getCount(), person));
                continue;
            }
            invetoryItem.setCount(invDTO.getCount());
            inventoryRepository.save(invetoryItem);
        }
    }
}
