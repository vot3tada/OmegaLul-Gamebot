package ru.gamebot.backend.controllers;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import ru.gamebot.backend.dto.InventoryDTO;
import ru.gamebot.backend.services.InventoryService;
import ru.gamebot.backend.util.exceptions.ItemExceptions.ItemNotFoundException;
import ru.gamebot.backend.util.exceptions.PersonExceptions.PersonErrorResponse;
import ru.gamebot.backend.util.exceptions.PersonExceptions.PersonNotFoundException;

import java.util.List;

@RestController
@RequestMapping("/api/inventory")
@RequiredArgsConstructor
@Slf4j
public class InventoryController {

    private final InventoryService inventoryService;

    @PutMapping("/update")
    public ResponseEntity<HttpStatus> updateInventory(@RequestBody InventoryDTO inventoryDTO){
        inventoryService.updateInventory(inventoryDTO);
        return new ResponseEntity<>(HttpStatus.NO_CONTENT);
    }

    @GetMapping("/id/{chatId}/{userId}")
    public List<InventoryDTO> getInventory(@PathVariable("chatId") Integer chatId,
                                           @PathVariable("userId") Integer userId){

        return inventoryService.getAllItemsInInventory(chatId, userId);
    }


    @DeleteMapping("/delete")
    public ResponseEntity<HttpStatus> deleteItemFromInventory(@RequestBody InventoryDTO inventoryDTO){
        inventoryService.deleteItemFromInventory(inventoryDTO);
        return new ResponseEntity<>(HttpStatus.NO_CONTENT);
    }

    @ExceptionHandler
    private ResponseEntity<PersonErrorResponse> handleException (ItemNotFoundException e){
        PersonErrorResponse response = new PersonErrorResponse("Item not found");
        return new ResponseEntity<>(response, HttpStatus.NOT_FOUND);
    }

    @ExceptionHandler
    private ResponseEntity<PersonErrorResponse> handleException (PersonNotFoundException e){
        PersonErrorResponse response = new PersonErrorResponse("Person with this id wasn`t found!");
        return new ResponseEntity<>(response, HttpStatus.NOT_FOUND);
    }

}
