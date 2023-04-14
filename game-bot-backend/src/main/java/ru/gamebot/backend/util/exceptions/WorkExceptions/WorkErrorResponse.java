package ru.gamebot.backend.util.exceptions.WorkExceptions;

import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.Setter;

@Setter
@Getter
@AllArgsConstructor
public class WorkErrorResponse {
    private String message;
}
