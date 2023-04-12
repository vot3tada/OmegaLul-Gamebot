package ru.gamebot.backend.dto;

import lombok.Data;

@Data
public class InventoryDTO {
    private Integer itemId;
    private Integer count;
    private Integer chatId;
    private Integer userId;

    public InventoryDTO(Integer itemId, Integer count){
        this.count= count;
        this.itemId = itemId;
    }
}
