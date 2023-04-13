package ru.gamebot.backend.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import ru.gamebot.backend.models.Inventory;
import ru.gamebot.backend.models.Person;

import java.util.List;

public interface InventoryRepository extends JpaRepository<Inventory, Integer> {
    Inventory findInventoryByItem_Id(Integer itemId);
    void deleteByItemIdAndPerson(Integer itemId, Person person);

    List<Inventory> findAllByPerson(Person person);
}
