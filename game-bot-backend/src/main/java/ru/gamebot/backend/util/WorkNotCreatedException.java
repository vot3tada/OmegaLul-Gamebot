package ru.gamebot.backend.util;

public class WorkNotCreatedException extends RuntimeException{
    public WorkNotCreatedException(String msg){
        super(msg);
    }
}
