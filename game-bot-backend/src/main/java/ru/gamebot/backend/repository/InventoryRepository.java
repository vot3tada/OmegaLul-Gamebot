package ru.gamebot.backend.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import ru.gamebot.backend.models.Inventory;
import ru.gamebot.backend.models.Item;
import ru.gamebot.backend.models.Person;

import java.util.List;
@Repository
public interface InventoryRepository extends JpaRepository<Inventory, Integer> {
    Inventory findInventoryByItemAndPerson(Item item, Person person);
    void deleteByItemIdAndPerson(Integer itemId, Person person);

    List<Inventory> findAllByPerson(Person person);
}
