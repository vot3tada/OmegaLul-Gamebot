package ru.gamebot.backend.dto;

import lombok.Data;

@Data
public class PersonEventsDTO {
    private Boolean creator;
    private Integer chatId;
    private Integer userId;

    public PersonEventsDTO(Boolean creator, Integer chatId, Integer userId) {
        this.creator = creator;
        this.chatId = chatId;
        this.userId = userId;
    }
}
