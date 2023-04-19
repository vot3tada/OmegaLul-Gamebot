package ru.gamebot.backend.controllers;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.validation.BindingResult;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.*;
import ru.gamebot.backend.dto.TaskDTO;
import ru.gamebot.backend.dto.UpdateTaskDTO;
import ru.gamebot.backend.services.TaskService;
import ru.gamebot.backend.util.exceptions.ErrorResponse;
import ru.gamebot.backend.util.exceptions.PersonExceptions.PersonNotFoundException;
import ru.gamebot.backend.util.exceptions.TaskExceptions.TaskNotFoundException;
import ru.gamebot.backend.util.exceptions.TaskExceptions.TaskNotUpdateException;

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

    @GetMapping("/person/{ownerUserId}/{chatId}")
    public List<TaskDTO> getPersonTasks(@PathVariable("chatId") Integer chatId
                                            ,@PathVariable("ownerUserId") Integer ownerUserId){
        return taskService.personTasks(ownerUserId, chatId);
    }

    @PostMapping("/create")
    public ResponseEntity<HttpStatus> createTask(@RequestBody TaskDTO taskDTO){
        taskService.createTask(taskDTO);
        return new ResponseEntity<>(HttpStatus.CREATED);
    }

    @PutMapping("/update")
    public ResponseEntity<HttpStatus> updateTask(@RequestBody @Validated UpdateTaskDTO updateTaskDTO
                                                , BindingResult bindingResult){
        if(bindingResult.hasErrors()){
            StringBuilder errorMsg = new StringBuilder();
            var error =bindingResult.getFieldError();
            errorMsg.append(error.getField())
                    .append(" - ").append(error.getDefaultMessage())
                    .append(";");
            throw new TaskNotUpdateException(errorMsg.toString());
        }
        taskService.updateTask(updateTaskDTO);
        return new ResponseEntity<>(HttpStatus.NO_CONTENT);
    }

    @DeleteMapping("/delete/{id}")
    public ResponseEntity<HttpStatus> deleteTask(@PathVariable("id") Integer id){
        taskService.taskDelete(id);
        return new ResponseEntity<>(HttpStatus.NO_CONTENT);
    }

    @ExceptionHandler
    private ResponseEntity<ErrorResponse> handleException (PersonNotFoundException e){
        ErrorResponse response = new ErrorResponse("Person not found!");
        return new ResponseEntity<>(response, HttpStatus.NOT_FOUND);
    }

    @ExceptionHandler
    private ResponseEntity<ErrorResponse> handleException (TaskNotFoundException e){
        ErrorResponse response = new ErrorResponse("Task not found!");
        return new ResponseEntity<>(response, HttpStatus.NOT_FOUND);
    }

    @ExceptionHandler
    private ResponseEntity<ErrorResponse> handleException (TaskNotUpdateException e){
        ErrorResponse response = new ErrorResponse(e.getMessage());
        return new ResponseEntity<>(response, HttpStatus.BAD_REQUEST);
    }

}
