package ru.gamebot.backend.controllers;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.validation.BindingResult;
import org.springframework.validation.FieldError;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.*;
import ru.gamebot.backend.dto.Create;
import ru.gamebot.backend.dto.PersonDTO;
import ru.gamebot.backend.services.PersonService;
import ru.gamebot.backend.util.exceptions.ErrorResponse;
import ru.gamebot.backend.util.exceptions.GitlabCleintExceptions.GitlabUserNotFound;
import ru.gamebot.backend.util.exceptions.PersonExceptions.*;

import java.util.List;

@RestController
@RequestMapping("/api/person")
@RequiredArgsConstructor
@Slf4j
public class PersonController {

    private final PersonService personService;

    @GetMapping("/id/{chatId}")
    public List<PersonDTO> getAllPersonsFromChat(@PathVariable("chatId") int chatId){
        return personService.getPersonsByChatId(chatId);
    }

    @GetMapping("/all")
    public List<PersonDTO> getAllPersons (){
        return personService.getAllPersons();
    }

    @PutMapping("/update")
    public ResponseEntity<HttpStatus> updatePerson(@RequestParam(name = "chatId") int chatId,
                                                   @RequestParam(name = "userId") int userId,
                                                   @RequestBody PersonDTO personDTO){

        personService.updatePerson(personDTO, chatId, userId);
        return new ResponseEntity<>(HttpStatus.NO_CONTENT);
    }

    @DeleteMapping("/delete/{chatId}")
    public ResponseEntity<HttpStatus> deleteAllPersonsByChatId(@PathVariable("chatId") int chatId){
        personService.deletePersonsByChatId(chatId);
        return new ResponseEntity<>(HttpStatus.NO_CONTENT);
    }
    @PostMapping("/create")
    public ResponseEntity<HttpStatus> createPerson(@RequestBody @Validated(Create.class)
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

        personService.createPerson(personDTO);
        return new ResponseEntity<>(HttpStatus.CREATED);
    }

    @ExceptionHandler
    private ResponseEntity<ErrorResponse> handleException (PersonNotFoundException e){
        ErrorResponse response = new ErrorResponse("Person with this id wasn`t found!");
        return new ResponseEntity<>(response, HttpStatus.NOT_FOUND);
    }

    @ExceptionHandler
    private ResponseEntity<ErrorResponse> handleException (PersonChatIdNotFound e){
        ErrorResponse response = new ErrorResponse("Person with this chatId wasn`t found!");
        return new ResponseEntity<>(response, HttpStatus.NOT_FOUND);
    }

    @ExceptionHandler
    private ResponseEntity<ErrorResponse> handleException (PersonNotUpdateException e){
        ErrorResponse response = new ErrorResponse(e.getMessage());
        return new ResponseEntity<>(response, HttpStatus.BAD_REQUEST);
    }

    @ExceptionHandler
    private ResponseEntity<ErrorResponse> handleException (PersonNotCreateException e){
        ErrorResponse response = new ErrorResponse(e.getMessage());
        return new ResponseEntity<>(response, HttpStatus.BAD_REQUEST);
    }

    @ExceptionHandler
    private ResponseEntity<ErrorResponse> handleException (PersonAlreadyExistsException e){
        ErrorResponse response = new ErrorResponse("Person already exists");
        return new ResponseEntity<>(response, HttpStatus.BAD_REQUEST);
    }

    @ExceptionHandler
    private ResponseEntity<ErrorResponse> handleException (GitlabUserNotFound e){
        ErrorResponse response = new ErrorResponse(e.getMessage());
        return new ResponseEntity<>(response, HttpStatus.NOT_FOUND);
    }
}
