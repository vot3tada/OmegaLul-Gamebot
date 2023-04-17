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
import ru.gamebot.backend.dto.CreateEventDTO;
import ru.gamebot.backend.dto.GetEventDTO;
import ru.gamebot.backend.services.EventService;
import ru.gamebot.backend.util.exceptions.ErrorResponse;
import ru.gamebot.backend.util.exceptions.EventExceptions.ChatNotFoundException;
import ru.gamebot.backend.util.exceptions.EventExceptions.EventAlreadyExistException;
import ru.gamebot.backend.util.exceptions.EventExceptions.EventNotCreateException;
import ru.gamebot.backend.util.exceptions.EventExceptions.EventNotFoundException;
import ru.gamebot.backend.util.exceptions.PersonExceptions.PersonNotFoundException;

import java.util.List;

@RestController
@RequestMapping("/api/event")
@RequiredArgsConstructor
@Slf4j
public class EventController {
    private final EventService eventService;

    @GetMapping("id/{id}")
    public GetEventDTO getEvent(@PathVariable("id") Integer id){
        return eventService.getEventById(id);
    }

    @GetMapping("/chat/{chatId}")
    public List<GetEventDTO> getEvents(@PathVariable("chatId") Integer chatId){
        return eventService.getEventsByChatId(chatId);
    }

    @PostMapping("/create")
    public ResponseEntity<GetEventDTO> createEvent(@RequestBody @Validated(Create.class) CreateEventDTO createEventDTO
                                                    ,BindingResult bindingResult){
        if(bindingResult.hasErrors()){
            StringBuilder errorMsg = new StringBuilder();
            List<FieldError> errors = bindingResult.getFieldErrors();
            for(FieldError error : errors){
                errorMsg.append(error.getField())
                        .append(" - ").append(error.getDefaultMessage())
                        .append(";");
            }
            throw new EventNotCreateException(errorMsg.toString());
        }
        var event = eventService.createEvent(createEventDTO);
        return new ResponseEntity<>(event,HttpStatus.CREATED);
    }

    @PostMapping("/add-member")
    public ResponseEntity<HttpStatus> addMemberToEvent(@RequestBody CreateEventDTO eventDTO){
        eventService.addMember(eventDTO);
        return new ResponseEntity<>(HttpStatus.CREATED);
    }

    @DeleteMapping("/delete-member")
    public ResponseEntity<HttpStatus> deleteMemberToEvent(@RequestBody CreateEventDTO eventDTO){
        eventService.deleteMember(eventDTO);
        return new ResponseEntity<>(HttpStatus.NO_CONTENT);
    }
    @ExceptionHandler
    public ResponseEntity<ErrorResponse> handleException(PersonNotFoundException e){
        var response = new ErrorResponse("Person not found!");
        return new ResponseEntity<>(response,HttpStatus.NOT_FOUND);
    }

    @ExceptionHandler
    public ResponseEntity<ErrorResponse> handleException(EventNotCreateException e){
        var response = new ErrorResponse(e.getMessage());
        return new ResponseEntity<>(response,HttpStatus.BAD_REQUEST);
    }

    @ExceptionHandler
    public ResponseEntity<ErrorResponse> handleException(EventAlreadyExistException e){
        var response = new ErrorResponse("Event not found!");
        return new ResponseEntity<>(response,HttpStatus.BAD_REQUEST);
    }

    @ExceptionHandler
    public ResponseEntity<ErrorResponse> handleException(ChatNotFoundException e){
        var response = new ErrorResponse(e.getMessage());
        return new ResponseEntity<>(response,HttpStatus.BAD_REQUEST);
    }

    @ExceptionHandler
    public ResponseEntity<ErrorResponse> handleException(EventNotFoundException e){
        var response = new ErrorResponse("Event not found!");
        return new ResponseEntity<>(response,HttpStatus.NOT_FOUND);
    }
}
