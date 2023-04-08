package ru.gamebot.backend.util;

public class PersonNotUpdateException extends RuntimeException{
    public PersonNotUpdateException(String msg){
        super(msg);
    }
}
