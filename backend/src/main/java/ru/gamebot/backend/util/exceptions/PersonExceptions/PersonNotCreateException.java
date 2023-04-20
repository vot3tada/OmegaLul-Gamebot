package ru.gamebot.backend.util.exceptions.PersonExceptions;

public class PersonNotCreateException extends  RuntimeException{
    public PersonNotCreateException(String msg){
        super(msg);
    }
}
