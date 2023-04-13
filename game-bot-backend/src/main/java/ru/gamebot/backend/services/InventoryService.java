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
import ru.gamebot.backend.util.ItemExceptions.ItemNotFoundException;
import ru.gamebot.backend.util.PersonExceptions.PersonNotFoundException;

import java.util.ArrayList;
import java.util.List;

@Service
@Transactional(readOnly = true)
@RequiredArgsConstructor
public class InventoryService {

    private final PersonRepository personRepository;
    private final ItemRepository itemRepository;
    private final InventoryRepository inventoryRepository;

    public List<InventoryDTO> getAllItemsInInventory(Integer chatId, Integer userId){
        var inventory = inventoryRepository.findAllByPerson(personRepository.findById(new PersonPK(chatId, userId))
                                                            .orElseThrow(PersonNotFoundException::new));
        List<InventoryDTO> inventoryDTO = new ArrayList<>();
        for(Inventory inv: inventory){
            inventoryDTO.add(new InventoryDTO(inv.getItem().getId(), inv.getCount(), chatId, userId));
        }
        return inventoryDTO;
    }

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
    public void deleteItemFromInventory(InventoryDTO inventoryDTO){
        var person = personRepository.findById(new PersonPK(inventoryDTO.getChatId(), inventoryDTO.getUserId()))
                                                .orElseThrow(PersonNotFoundException::new);
        itemRepository.findById(inventoryDTO.getItemId()).orElseThrow(ItemNotFoundException::new);
        inventoryRepository.deleteByItemIdAndPerson(inventoryDTO.getItemId(), person);
    }
}

