package ru.gamebot.backend.controllers;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import ru.gamebot.backend.dto.AchievementDTO;
import ru.gamebot.backend.dto.PersonAchievementDTO;
import ru.gamebot.backend.services.AchievementService;
import ru.gamebot.backend.util.exceptions.AchievementExceptions.AchievementNotFoundException;
import ru.gamebot.backend.util.exceptions.ErrorResponse;
import ru.gamebot.backend.util.exceptions.PersonExceptions.PersonNotFoundException;

import java.util.List;

@RestController
@RequestMapping("/api/achievement")
@RequiredArgsConstructor
@Slf4j
public class AchievementController {
    private final AchievementService achievementService;

    @GetMapping("/person/{chatId}/{userId}")
    public List<AchievementDTO> getPersonAchievement(@PathVariable("chatId") Integer chatId
                                                    ,@PathVariable("userId") Integer userId){
        return achievementService.getPersonAchievements(chatId, userId);
    }

    @GetMapping("/id/{id}")
    public AchievementDTO getAchievement(@PathVariable("id") String id){
        return achievementService.getAchievementById(id);
    }

    @PostMapping("/person/add")
    public ResponseEntity<HttpStatus> addAchievementToPerson(@RequestBody PersonAchievementDTO personAchievementDTO){
        achievementService.addAchievementToPerson(personAchievementDTO);
        return new ResponseEntity<>(HttpStatus.CREATED);
    }

    @ExceptionHandler
    public ResponseEntity<ErrorResponse> handleException(PersonNotFoundException e){
        var response = new ErrorResponse("Person not found!");
        return new ResponseEntity<>(response,HttpStatus.NOT_FOUND);
    }

    @ExceptionHandler
    public ResponseEntity<ErrorResponse> handleException(AchievementNotFoundException e){
        var response = new ErrorResponse("Achievement not found!");
        return new ResponseEntity<>(response,HttpStatus.NOT_FOUND);
    }
}
