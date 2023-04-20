package ru.gamebot.backend.util.exceptions.PersonExceptions;

public class PersonNotUpdateException extends RuntimeException{
    public PersonNotUpdateException(String msg){
        super(msg);
    }
}
