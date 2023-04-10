package ru.gamebot.backend.services;

import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import ru.gamebot.backend.models.Item;
import ru.gamebot.backend.repository.ItemRepository;
import ru.gamebot.backend.util.ItemNotFoundException;

@Service
@Transactional(readOnly = true)
@RequiredArgsConstructor
public class ItemService {

    private final ItemRepository itemRepository;

    public Item getItemById(Integer id){
        return itemRepository.findById(id).orElseThrow(ItemNotFoundException::new);
    }

    @Transactional
    public void addItemAndEffect(Item item){
        itemRepository.save(item);
    }

    @Transactional
    public void deleteItemById(Integer id){
        Item item = getItemById(id);
        itemRepository.delete(item);
    }

}
