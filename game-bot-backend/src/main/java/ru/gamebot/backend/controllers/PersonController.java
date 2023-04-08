package ru.gamebot.backend.controllers;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.validation.BindingResult;
import org.springframework.validation.FieldError;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.*;
import ru.gamebot.backend.dto.CreatePerson;
import ru.gamebot.backend.dto.PersonDTO;
import ru.gamebot.backend.models.Person;
import ru.gamebot.backend.services.PersonService;
import ru.gamebot.backend.util.*;

import java.util.ArrayList;
import java.util.List;

@RestController
@RequestMapping("/api/person")
@RequiredArgsConstructor
@Slf4j
public class PersonController {

    private final PersonService personService;
    private final PersonMapper personMapper;


    @GetMapping("/id/{chatId}")
    public List<PersonDTO> getPersonByChatId(@PathVariable("chatId") int chatId){
        return convertToListPersonDTO(personService.getPersonsByChatId(chatId));
    }

    @GetMapping("/all")
    public List<PersonDTO> getAllPersonsFromChat(){
        return convertToListPersonDTO(personService.getAllPersons());
    }

    @PutMapping("/update")
    public ResponseEntity<HttpStatus> updatePerson(@RequestParam("chatId") int chatId,
                                                   @RequestParam("userId") int userId,
                                                   @RequestBody PersonDTO personDTO){

        Person person = personService.getPerson(chatId,userId);
        if (personDTO.getExperience()!=null && person.getExperience()!=null && person.getExperience() > personDTO.getExperience()){
            throw new PersonNotUpdateException("Experience cannot be less than what is already available!");
        }

        personDTO.setPersonPKDTO(new PersonDTO.PersonPKDTO(chatId, userId));

        Person convertedPerson = convertToPerson(personDTO);
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

    @ExceptionHandler
    private ResponseEntity<PersonErrorResponse> handleException (PersonAlreadyExistsException e){
        PersonErrorResponse response = new PersonErrorResponse("Person already exists");
        return new ResponseEntity<>(response, HttpStatus.BAD_REQUEST);
    }

    private Person convertToPerson(PersonDTO personDTO){
        return personMapper.personDtoToPerson(personDTO);
    }

    private List<PersonDTO> convertToListPersonDTO(List<Person> persons){
        List<PersonDTO> personDTOS = new ArrayList<>();
        for(Person person: persons){
            personDTOS.add(personMapper.personToPersonDTO(person));
        }
        return  personDTOS;
    }

}
