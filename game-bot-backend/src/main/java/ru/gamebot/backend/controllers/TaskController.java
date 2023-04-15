package ru.gamebot.backend.controllers;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import ru.gamebot.backend.dto.TaskDTO;
import ru.gamebot.backend.services.TaskService;

import java.util.List;

@RestController
@RequestMapping("/api/task")
@RequiredArgsConstructor
@Slf4j
public class TaskController {

    private final TaskService taskService;


    @GetMapping("/all")
    public List<TaskDTO> getAllTasks(){
        return taskService.allTasks();
    }

    @GetMapping("/free")
    public List<TaskDTO> getFreeTasks(){
        return taskService.freeTasks();
    }

    @GetMapping("/taken/{workerUserId}/{chatId}")
    public List<TaskDTO> getTakenTasks(@PathVariable("chatId") Integer chatId
                                        ,@PathVariable("workerUserId") Integer workerUserId){
        return taskService.takenTasks(workerUserId, chatId);
    }

    @GetMapping("/complete/{ownerUserId}/{chatId}")
    public List<TaskDTO> getPersonTasks(@PathVariable("chatId") Integer chatId
                                            ,@PathVariable("ownerUserId") Integer ownerUserId){
        return taskService.personTasks(ownerUserId, chatId);
    }

    @PostMapping("/create")
    public ResponseEntity<HttpStatus> createTask(@RequestBody TaskDTO taskDTO){
        taskService.createTask(taskDTO);
        return new ResponseEntity<>(HttpStatus.CREATED);
    }
}
