package ru.gamebot.backend.util.exceptions.GitlabCleintExceptions;

public class GitlabUserNotFound extends RuntimeException{
    public GitlabUserNotFound(String msg){
        super(msg);
    }
}
