package ru.gamebot.backend.util.PersonExceptions;

public class PersonNotCreateException extends  RuntimeException{
    public PersonNotCreateException(String msg){
        super(msg);
    }
}
