package ru.gamebot.backend.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import ru.gamebot.backend.models.Item;

public interface ItemRepository extends JpaRepository<Item, Integer> {

}
