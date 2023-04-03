package ru.gamebot.backend.controllers;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import ru.gamebot.backend.models.Person;
import ru.gamebot.backend.services.PersonService;
import ru.gamebot.backend.util.PersonErrorResponse;
import ru.gamebot.backend.util.PersonNotFoundException;

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


    @ExceptionHandler
    private ResponseEntity<PersonErrorResponse> handleException (PersonNotFoundException e){
        PersonErrorResponse response = new PersonErrorResponse("Person with this id wasn`t found!");
        return new ResponseEntity<>(response, HttpStatus.NOT_FOUND);
    }
}
