package ru.gamebot.backend.util.PersonExceptions;

public class PersonNotUpdateException extends RuntimeException{
    public PersonNotUpdateException(String msg){
        super(msg);
    }
}
