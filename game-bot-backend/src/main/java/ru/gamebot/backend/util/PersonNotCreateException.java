package ru.gamebot.backend.util;

public class PersonNotCreateException extends  RuntimeException{
    public PersonNotCreateException(String msg){
        super(msg);
    }
}
