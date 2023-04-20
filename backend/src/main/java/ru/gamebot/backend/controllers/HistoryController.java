package ru.gamebot.backend.controllers;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.validation.BindingResult;
import org.springframework.validation.FieldError;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.*;
import ru.gamebot.backend.dto.HistoryDTO;
import ru.gamebot.backend.services.HistoryService;
import ru.gamebot.backend.util.exceptions.ErrorResponse;
import ru.gamebot.backend.util.exceptions.HistoryExceptions.HistoryNotExistsException;
import ru.gamebot.backend.util.exceptions.HistoryExceptions.HistoryNotFoundException;
import ru.gamebot.backend.util.exceptions.HistoryExceptions.HistoryNotUpdateException;

import java.util.List;

@RestController
@RequestMapping("/api/history")
@RequiredArgsConstructor
@Slf4j
public class HistoryController {
    private final HistoryService historyService;

    @GetMapping("/id/{chatId}/{userId}")
    public HistoryDTO getHistory(@PathVariable("chatId") Integer chatId, @PathVariable("userId") Integer userId){
        return historyService.getHistory(chatId,userId);
    }
    @PutMapping("/update")
    public ResponseEntity<HttpStatus> updateHistory(@RequestBody @Validated HistoryDTO historyDTO
                                                    , BindingResult bindingResult){
        if(bindingResult.hasErrors()){
            StringBuilder errorMsg = new StringBuilder();
            List<FieldError> errors = bindingResult.getFieldErrors();
            for(FieldError error : errors){
                errorMsg.append(error.getField())
                        .append(" - ").append(error.getDefaultMessage())
                        .append(";");
            }
            throw new HistoryNotUpdateException(errorMsg.toString());
        }
        historyService.updateHistory(historyDTO);
        return new ResponseEntity<>(HttpStatus.NO_CONTENT);
    }

    @ExceptionHandler
    public ResponseEntity<ErrorResponse> handleException(HistoryNotUpdateException e){
        var response = new ErrorResponse(e.getMessage());
        return new ResponseEntity<>(response,HttpStatus.BAD_REQUEST);
    }

    @ExceptionHandler
    public ResponseEntity<ErrorResponse> handleException(HistoryNotExistsException e){
        var response = new ErrorResponse(e.getMessage());
        return new ResponseEntity<>(response,HttpStatus.BAD_REQUEST);
    }

    @ExceptionHandler
    public ResponseEntity<ErrorResponse> handleException(HistoryNotFoundException e){
        var response = new ErrorResponse("History with this id not found!");
        return new ResponseEntity<>(response,HttpStatus.BAD_REQUEST);
    }

}


