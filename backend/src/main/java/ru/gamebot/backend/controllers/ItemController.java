package ru.gamebot.backend.controllers;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import ru.gamebot.backend.dto.ItemDTO;
import ru.gamebot.backend.services.ItemService;
import ru.gamebot.backend.util.exceptions.ErrorResponse;
import ru.gamebot.backend.util.exceptions.ItemExceptions.ItemNotFoundException;

import java.util.List;

@RestController
@RequestMapping("/api/item")
@RequiredArgsConstructor
@Slf4j
public class ItemController {

    private final ItemService itemService;

    @GetMapping("/all")
    public List<ItemDTO> getAllItems(){
        return itemService.getAllItems();
    }

    @GetMapping("/id/{id}")
    public ItemDTO getItem(@PathVariable Integer id){
        return itemService.getItemById(id);
    }

    @GetMapping("/type/{type}")
    public List<ItemDTO> getItemsByType(@PathVariable("type") String type){
        return itemService.getItemsByType(type);
    }
    @PostMapping("/create")
    public ResponseEntity<HttpStatus> createItem(@RequestBody ItemDTO itemDTO){
        itemService.addItemAndEffect(itemDTO);
        return new ResponseEntity<>(HttpStatus.CREATED);
    }

    @DeleteMapping("/delete/{id}")
    public ResponseEntity<HttpStatus> deleteItem(@PathVariable Integer id){

        itemService.deleteItemById(id);
        return new ResponseEntity<>(HttpStatus.NO_CONTENT);
    }

    @ExceptionHandler
    private ResponseEntity<ErrorResponse> handleException (ItemNotFoundException e){
        ErrorResponse response = new ErrorResponse("Item with this id wasn`t found!");
        return new ResponseEntity<>(response, HttpStatus.NOT_FOUND);
    }
}
