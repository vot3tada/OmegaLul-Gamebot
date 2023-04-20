package ru.gamebot.backend.util.exceptions.EventExceptions;

public class EventAlreadyExistException extends RuntimeException{
    public EventAlreadyExistException(String msg){
        super(msg);
    }
}
