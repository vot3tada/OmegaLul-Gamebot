package ru.gamebot.backend.util.exceptions.EventExceptions;

public class ChatNotFoundException extends RuntimeException{
    public ChatNotFoundException(String msg){
        super(msg);
    }
}
