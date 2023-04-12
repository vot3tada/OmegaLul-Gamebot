package ru.gamebot.backend.util.ItemExceptions;

import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.Setter;

@Setter
@Getter
@AllArgsConstructor
public class ItemErrorResponse {
    private String message;
}
