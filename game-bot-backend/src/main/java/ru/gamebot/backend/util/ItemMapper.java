package ru.gamebot.backend.util;

import org.mapstruct.InjectionStrategy;
import org.mapstruct.Mapper;
import ru.gamebot.backend.dto.ItemDTO;
import ru.gamebot.backend.models.Item;


    @Mapper(
            componentModel = "spring",
            injectionStrategy = InjectionStrategy.CONSTRUCTOR
    )
    public interface ItemMapper {
        Item itemDTOToItem(ItemDTO source);

        ItemDTO itemToItemDTO(Item source);
    }
