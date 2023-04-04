package ru.gamebot.backend.controllers;

import org.modelmapper.ModelMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.validation.BindingResult;
import org.springframework.validation.FieldError;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.*;
import ru.gamebot.backend.dto.CreatePerson;
import ru.gamebot.backend.dto.PersonDTO;
import ru.gamebot.backend.models.Person;
import ru.gamebot.backend.models.PersonPK;
import ru.gamebot.backend.services.PersonService;
import ru.gamebot.backend.util.PersonErrorResponse;
import ru.gamebot.backend.util.PersonNotCreateException;
import ru.gamebot.backend.util.PersonNotFoundException;
import ru.gamebot.backend.util.PersonNotUpdateException;

import java.util.List;

@RestController
@RequestMapping("/api/person")
public class PersonController {

    private final PersonService personService;

    @Autowired
    public PersonController(PersonService personService){
        this.personService = personService;
    }
    @GetMapping("/id")
    public Person getPersonByID(@RequestParam(defaultValue = "empty") int chatId,
                                @RequestParam(defaultValue = "empty") int userId){
        return personService.getPerson(chatId,userId);
    }

    @GetMapping("/all")
    public List<Person> getAllPersons(){
        return personService.getAllPersons();
    }

    @PutMapping("/update")
    public ResponseEntity<HttpStatus> updatePerson(@RequestParam(defaultValue = "empty") int chatId,
                                                   @RequestParam(defaultValue = "empty") int userId,
                                                   @RequestBody PersonDTO personDTO){

        Person person = personService.getPerson(chatId,userId);
        if (person.getExperience() > personDTO.getExperience()){
            throw new PersonNotUpdateException("Experience cannot be less than what is already available!");
        }
        Person convertedPerson = convertToPerson(personDTO, person);
        personService.updatePerson(convertedPerson);
        return new ResponseEntity<>(HttpStatus.NO_CONTENT);
    }

    @PostMapping("/create")
    public ResponseEntity<HttpStatus> createPerson(@RequestBody @Validated(CreatePerson.class)
                                                       PersonDTO personDTO, BindingResult bindingResult){

        if(bindingResult.hasErrors()){
            StringBuilder errorMsg = new StringBuilder();
            List<FieldError> errors = bindingResult.getFieldErrors();
            for(FieldError error : errors){
                errorMsg.append(error.getField())
                        .append(" - ").append(error.getDefaultMessage())
                        .append(";");
            }
            throw new PersonNotCreateException(errorMsg.toString());
        }

        Person convertedPerson = convertToPerson(personDTO);
        personService.createPerson(convertedPerson);
        return new ResponseEntity<>(HttpStatus.CREATED);
    }

    @ExceptionHandler
    private ResponseEntity<PersonErrorResponse> handleException (PersonNotFoundException e){
        PersonErrorResponse response = new PersonErrorResponse("Person with this id wasn`t found!");
        return new ResponseEntity<>(response, HttpStatus.NOT_FOUND);
    }

    @ExceptionHandler
    private ResponseEntity<PersonErrorResponse> handleException (PersonNotUpdateException e){
        PersonErrorResponse response = new PersonErrorResponse(e.getMessage());
        return new ResponseEntity<>(response, HttpStatus.BAD_REQUEST);
    }

    @ExceptionHandler
    private ResponseEntity<PersonErrorResponse> handleException (PersonNotCreateException e){
        PersonErrorResponse response = new PersonErrorResponse(e.getMessage());
        return new ResponseEntity<>(response, HttpStatus.BAD_REQUEST);
    }

    private Person convertToPerson(PersonDTO personDTO, Person person){
        ModelMapper modelMapper = new ModelMapper();
        modelMapper.getConfiguration().setSkipNullEnabled(true);
        modelMapper.map(personDTO,person);
        return person;
    }

    private Person convertToPerson(PersonDTO personDTO){
        ModelMapper modelMapper = new ModelMapper();
        PersonPK personPK = new PersonPK(personDTO.getChatId(), personDTO.getUserId());
        Person person = modelMapper.map(personDTO, Person.class);
        person.setPersonPk(personPK);
        return person;
    }

}
