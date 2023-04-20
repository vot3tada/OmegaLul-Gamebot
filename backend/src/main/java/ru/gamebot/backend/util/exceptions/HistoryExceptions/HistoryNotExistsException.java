package ru.gamebot.backend.util.exceptions.HistoryExceptions;

public class HistoryNotExistsException extends RuntimeException{
    public HistoryNotExistsException(String msg){
        super(msg);
    }
}
