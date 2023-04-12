package ru.gamebot.backend.services;

import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import ru.gamebot.backend.dto.InventoryDTO;
import ru.gamebot.backend.models.Inventory;
import ru.gamebot.backend.models.PersonPK;
import ru.gamebot.backend.repository.InventoryRepository;
import ru.gamebot.backend.repository.ItemRepository;
import ru.gamebot.backend.repository.PersonRepository;
import ru.gamebot.backend.util.ItemNotFoundException;
import ru.gamebot.backend.util.PersonExceptions.PersonNotFoundException;

@Service
@Transactional(readOnly = true)
@RequiredArgsConstructor
public class InventoryService {

    private final PersonRepository personRepository;
    private final ItemRepository itemRepository;
    private final InventoryRepository inventoryRepository;

    @Transactional
    public void updateInventory(InventoryDTO inventoryDTO){
        var item = itemRepository.findById(inventoryDTO.getItemId()).orElseThrow(ItemNotFoundException::new);
        var invetoryItem = inventoryRepository.findInventoryByItem_Id(item.getId());
        var personPK = new PersonPK(inventoryDTO.getChatId(),inventoryDTO.getUserId());
        var person = personRepository.findById(personPK).orElseThrow(PersonNotFoundException::new);
        if (invetoryItem == null){
            inventoryRepository.save(new Inventory(item, inventoryDTO.getCount(), person));
            return;
        }
        invetoryItem.setCount(inventoryDTO.getCount());
        inventoryRepository.save(invetoryItem);
    }

    @Transactional
    public void deleteItemFromInventory(Integer itemId){
        itemRepository.findById(itemId).orElseThrow(ItemNotFoundException::new);
        inventoryRepository.deleteByItemId(itemId);
    }
}

