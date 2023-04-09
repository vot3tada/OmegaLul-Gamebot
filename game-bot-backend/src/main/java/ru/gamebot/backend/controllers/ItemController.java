package ru.gamebot.backend.controllers;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import ru.gamebot.backend.dto.ItemDTO;
import ru.gamebot.backend.services.ItemService;
import ru.gamebot.backend.util.ItemMapper;

@RestController
@RequestMapping("/api/item")
@RequiredArgsConstructor
@Slf4j
public class ItemController {

    private final ItemService itemService;
    private final ItemMapper itemMapper;

    @PostMapping("/create")
    public ResponseEntity<HttpStatus> createItem(@RequestBody ItemDTO itemDTO){
        itemService.addItemAndEffect(itemMapper.itemDTOToItem(itemDTO));
        return new ResponseEntity<>(HttpStatus.CREATED);
    }
}
