package ru.gamebot.backend.util.exceptions.HistoryExceptions;

public class HistoryNotUpdateException extends RuntimeException{
    public HistoryNotUpdateException(String msg){
        super(msg);
    }
}
