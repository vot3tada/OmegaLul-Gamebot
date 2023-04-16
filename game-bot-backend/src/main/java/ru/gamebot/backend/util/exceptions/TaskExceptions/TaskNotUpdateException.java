package ru.gamebot.backend.util.exceptions.TaskExceptions;

public class TaskNotUpdateException extends RuntimeException{
    public TaskNotUpdateException(String msg){
        super(msg);
    }
}
