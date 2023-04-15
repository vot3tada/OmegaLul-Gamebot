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
import ru.gamebot.backend.dto.WorkDTO;
import ru.gamebot.backend.services.WorkService;
import ru.gamebot.backend.util.exceptions.ErrorResponse;
import ru.gamebot.backend.util.exceptions.WorkExceptions.WorkAlreadyExistException;
import ru.gamebot.backend.util.exceptions.WorkExceptions.WorkNotCreatedException;
import ru.gamebot.backend.util.exceptions.WorkExceptions.WorkNotFoundException;

import java.util.List;

@RestController
@RequestMapping("/api/work")
@RequiredArgsConstructor
@Slf4j
public class WorkController {

    private final WorkService workService;

    @GetMapping("/all")
    public List<WorkDTO> getAllWorks(){
        return workService.getWorkList();
    }

    @PostMapping("/create")
    public ResponseEntity<HttpStatus> createWork(@RequestBody @Validated(Create.class)
                                               WorkDTO workDTO, BindingResult bindingResult){

        if(bindingResult.hasErrors()){
            StringBuilder errorMsg = new StringBuilder();
            List<FieldError> errors = bindingResult.getFieldErrors();
            for(FieldError error : errors){
                errorMsg.append(error.getField())
                        .append(" - ").append(error.getDefaultMessage())
                        .append(";");
            }
            throw new WorkNotCreatedException(errorMsg.toString());
        }

        workService.createWork(workDTO);
        return new ResponseEntity<>(HttpStatus.CREATED);
    }

    @DeleteMapping("/delete/{id}")
    public ResponseEntity<HttpStatus> deleteWork(@PathVariable("id") Integer id){
        workService.deleteWork(id);
        return new ResponseEntity<>(HttpStatus.NO_CONTENT);
    }

    @ExceptionHandler
    private ResponseEntity<ErrorResponse> handleException (WorkNotFoundException e){
        ErrorResponse response = new ErrorResponse("Work not found!");
        return new ResponseEntity<>(response, HttpStatus.NOT_FOUND);
    }

    @ExceptionHandler
    private ResponseEntity<ErrorResponse> handleException (WorkAlreadyExistException e){
        ErrorResponse response = new ErrorResponse("This work already exists!");
        return new ResponseEntity<>(response, HttpStatus.BAD_REQUEST);
    }

    @ExceptionHandler
    private ResponseEntity<ErrorResponse> handleException (WorkNotCreatedException e){
        ErrorResponse response = new ErrorResponse(e.getMessage());
        return new ResponseEntity<>(response, HttpStatus.BAD_REQUEST);
    }
}
