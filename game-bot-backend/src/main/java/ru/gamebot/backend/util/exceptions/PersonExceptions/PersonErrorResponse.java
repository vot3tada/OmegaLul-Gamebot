package ru.gamebot.backend.util.exceptions.PersonExceptions;

import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.Setter;

@Setter
@Getter
@AllArgsConstructor
public class PersonErrorResponse {
    private String message;
}
