package ru.gamebot.backend.util.PersonExceptions;

import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.Setter;

@Setter
@Getter
@AllArgsConstructor
public class PersonErrorResponse {
    private String message;
}
