package ru.gamebot.backend.controllers;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import ru.gamebot.backend.dto.BossDTO;
import ru.gamebot.backend.services.BossService;
import ru.gamebot.backend.util.exceptions.BossExceptions.BossNotFoundException;
import ru.gamebot.backend.util.exceptions.ErrorResponse;
import java.util.List;

@RestController
@RequestMapping("/api/boss")
@RequiredArgsConstructor
@Slf4j
public class BossController {
    private final BossService bossService;

    @GetMapping("/id/{id}")
    public BossDTO getBoss(@PathVariable("id") Integer id){
        return bossService.getBossById(id);
    }

    @GetMapping("/all")
    public List<BossDTO> getAllBoss(){
        return bossService.getALlBoss();
    }

    @ExceptionHandler
    public ResponseEntity<ErrorResponse> handleException(BossNotFoundException e){
        var response = new ErrorResponse("Boss not found!");
        return new ResponseEntity<>(response, HttpStatus.NOT_FOUND);
    }
}
