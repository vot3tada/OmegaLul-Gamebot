package ru.gamebot.backend.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import ru.gamebot.backend.models.Inventory;

public interface InventoryRepository extends JpaRepository<Inventory, Integer> {
    Inventory findInventoryByItem_Id(Integer itemId);
    void deleteByItemId(Integer id);
}
