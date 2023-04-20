package ru.gamebot.backend.dto;

import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
public class InventoryDTO {
    private Integer itemId;
    private Integer count;
    private Integer chatId;
    private Integer userId;

    public InventoryDTO(Integer itemId, Integer count, Integer chatId, Integer userId){
        this.count= count;
        this.chatId = chatId;
        this.userId = userId;
        this.itemId = itemId;
    }
}
