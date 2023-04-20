package ru.gamebot.backend.services;

import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import ru.gamebot.backend.dto.ItemDTO;
import ru.gamebot.backend.models.Item;
import ru.gamebot.backend.repository.EffectRepository;
import ru.gamebot.backend.repository.ItemRepository;
import ru.gamebot.backend.util.mappers.ItemMapper.ItemMapper;
import ru.gamebot.backend.util.exceptions.ItemExceptions.ItemNotFoundException;

import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;

@Service
@Transactional(readOnly = true)
@RequiredArgsConstructor
public class ItemService {

    private final ItemRepository itemRepository;
    private final EffectRepository effectRepository;
    private final ItemMapper itemMapper;

    public ItemDTO getItemById(Integer id){
        var item = itemRepository.findById(id).orElseThrow(ItemNotFoundException::new);
        return itemMapper.itemToItemDTO(item);
    }

    public List<ItemDTO> getAllItems(){
        var items = itemRepository.findAll();
        var itemsDTO = new ArrayList<ItemDTO>();
        for(Item item: items){
            itemsDTO.add(itemMapper.itemToItemDTO(item));
        }
        return itemsDTO;
    }

    @Transactional
    public void addItemAndEffect(ItemDTO itemDto){
        var effects = new HashSet<>(effectRepository.saveAll(itemDto.getEffects()));
        var item = itemMapper.itemDTOToItem(itemDto);
        item.setEffects(effects);
        itemRepository.save(item);
    }

    @Transactional
    public void deleteItemById(Integer id) {
        var item = itemRepository.findById(id).orElseThrow(ItemNotFoundException::new);
        effectRepository.deleteAll(item.getEffects());
        itemRepository.delete(item);
    }
}
