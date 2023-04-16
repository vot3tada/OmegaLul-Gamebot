package ru.gamebot.backend.util.exceptions.EventExceptions;

public class EventNotCreateException extends RuntimeException{
    public EventNotCreateException(String msg){
        super(msg);
    }
}
